# atlas/modules/core.py

from fastapi import APIRouter, Request

from ..state import AtlasState
from ..status import build_health
from ..config import Settings


class CoreModule:
    name = "core"

    def router(self, *, state: AtlasState, settings: Settings) -> APIRouter:
        r = APIRouter()

        @r.get("/health")
        def health():
            return build_health(state, settings=settings)

        @r.get("/whoami")
        def whoami(request: Request):
            return {
                "client_host": request.client.host if request.client else None,
                "method": request.method,
                "path": request.url.path,
                "user_agent": request.headers.get("user-agent"),
                "request_id": getattr(request.state, "request_id", None),
            }

        @r.get("/modules")
        def modules():
            return {
                "enabled_modules": settings.enabled_modules,
                "loaded_modules": ["core"],
                "version": settings.version,
            }

        return r
