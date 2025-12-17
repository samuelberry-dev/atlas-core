# atlas/main.py

import time
import uuid
import logging

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import HTTPException as StarletteHTTPException

from .state import AtlasState
from .config import Settings
from .errors import error_payload
from .modules.registry import load_modules

from pathlib import Path
from .storage.event_store import EventStore


logger = logging.getLogger("atlas")
logging.basicConfig(level=logging.INFO, format="%(message)s")

settings = Settings.load()
state = AtlasState()

DATA_DIR = Path("data")
event_store = EventStore(DATA_DIR / "atlas.db")

app = FastAPI(title="ATLAS Core", version=settings.version)


@app.middleware("http")
async def atlas_middleware(request: Request, call_next):
    start = time.perf_counter()

    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # count request
    state.mark_request()

    # auth: only enforced if ATLAS_API_KEY is set
    if settings.api_key is not None and request.url.path not in settings.open_paths:
        provided = request.headers.get("x-atlas-key")
        if provided != settings.api_key:
            latency_ms = int((time.perf_counter() - start) * 1000)
            logger.info(
                "event=request "
                f"request_id={request_id} "
                f"method={request.method} "
                f"path={request.url.path} "
                "status=401 "
                f"latency_ms={latency_ms} "
                f"client_host={(request.client.host if request.client else 'unknown')}"
            )
            return JSONResponse(
                status_code=401,
                content=error_payload(
                    code="unauthorized",
                    message="Missing or invalid X-ATLAS-KEY",
                    request_id=request_id,
                ),
                headers={"X-Request-ID": request_id},
            )

    response = await call_next(request)
    response.headers["X-Request-ID"] = request_id

    latency_ms = int((time.perf_counter() - start) * 1000)
    logger.info(
        "event=request "
        f"request_id={request_id} "
        f"method={request.method} "
        f"path={request.url.path} "
        f"status={response.status_code} "
        f"latency_ms={latency_ms} "
        f"client_host={(request.client.host if request.client else 'unknown')}"
    )

    return response


# ----- Exception Handling -----

@app.exception_handler(StarletteHTTPException)
async def http_exception_handler(request: Request, exc: StarletteHTTPException):
    request_id = getattr(request.state, "request_id", None)
    return JSONResponse(
        status_code=exc.status_code,
        content=error_payload(
            code="http_error",
            message=str(exc.detail),
            request_id=request_id,
        ),
        headers={"X-Request-ID": request_id} if request_id else None,
    )


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    request_id = getattr(request.state, "request_id", None)

    logger.info(
        "event=error "
        f"request_id={request_id} "
        f"path={request.url.path} "
        f"type={type(exc).__name__} "
        "message=unhandled_exception"
    )

    return JSONResponse(
        status_code=500,
        content=error_payload(
            code="internal_error",
            message="Internal server error",
            request_id=request_id,
        ),
        headers={"X-Request-ID": request_id} if request_id else None,
    )


# ----- Module loading -----

_loaded = load_modules(settings.enabled_modules)

for m in _loaded:
    app.include_router(m.router(state=state, settings=settings))


@app.get("/modules")
def modules():
    return {
        "enabled_modules": settings.enabled_modules,
        "loaded_modules": [m.name for m in _loaded],
        "version": settings.version,
        "auth_enabled": settings.api_key is not None,
        "open_paths": settings.open_paths,
    }
