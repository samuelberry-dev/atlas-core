# atlas/main.py

from fastapi import FastAPI, Request

from .state import AtlasState
from .status import build_health

app = FastAPI(
    title="ATLAS Core",
    version="0.0.2",
)

state = AtlasState()

@app.middleware("http")
async def request_counter(request: Request, call_next):
    """
    FastAPI that runs on EVERY request.
    """
    state.mark_request()

    response = await call_next(request)
    return response

@app.get("/health")
def health():
    """
    Health endpoint.
    """
    return build_health(state)

@app.get("/whoami")
def whoami(request: Request):
    """
    Debug endpoint.
    """
    return {
        "client_host": request.client.host if request.client else None,
        "method": request.method,
        "path": request.url.path,
        "user_agent": request.headers.get("user-agent"),
    }
