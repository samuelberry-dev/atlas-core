# atlas/errors.py

from typing import Any, Dict, Optional


def error_payload(
    *,
    code: str,
    message: str,
    request_id: Optional[str] = None,
    details: Optional[Dict[str, Any]] = None,
) -> Dict[str, Any]:
    payload: Dict[str, Any] = {
        "error": {
            "code": code,
            "message": message,
        }
    }
    if request_id:
        payload["error"]["request_id"] = request_id
    if details:
        payload["error"]["details"] = details
    return payload
