# atlas/main.py

import os
import time
import uuid
import logging
from typing import Optional

from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse

from .state import AtlasState
from .status import build_health

# ---------- Logging ----------
logger = logging.getLogger("atlas")
logging.basicConfig(
    level=logging.INFO,
    format="%(message)s",
)

# ---------- App ----------
app = FastAPI(
    title="ATLAS Core",
    version="0.0.2",
)

state = AtlasState()

def get_api_key() -> Optional[str]:
    """
    Reads the server API key from env.
    """
    key = os.getenv("ATLAS_API_KEY", "").strip()
    return key if key else None

def is_health_or_whoami(path: str) -> bool:
    return path in ("/health", "/whoami")

@app.middleware("http")
async def atlas_middleware(request: Request, call_next):

    start = time.perf_counter()

    # Generate a request ID
    request_id = str(uuid.uuid4())
    request.state.request_id = request_id

    # Count request
    state.mark_request()

    # Auth
    api_key = get_api_key()
    if api_key is not None and not is_health_or_whoami(request.url.path):
        provided = request.headers.get("x-atlas-key")
        if provided != api_key:
            latency_ms = int((time.perf_counter() - start) * 1000)
            # Log the rejected request
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
                content={
                    "error": "unauthorized",
                    "message": "Missing or invalid X-ATLAS-KEY",
                    "request_id": request_id,
                },
                headers={"X-Request-ID": request_id},
            )

    # Continue request
    response = await call_next(request)

    # Attach request ID to response headers
    response.headers["X-Request-ID"] = request_id

    # Log success/failure
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

@app.get("/health")
def health():
    return build_health(state)

@app.get("/whoami")
def whoami(request: Request):
    return {
        "client_host": request.client.host if request.client else None,
        "method": request.method,
        "path": request.url.path,
        "user_agent": request.headers.get("user-agent"),
        "request_id": getattr(request.state, "request_id", None),
    }

@app.get("/protected/ping")
def protected_ping():
    return {"ok": True}
