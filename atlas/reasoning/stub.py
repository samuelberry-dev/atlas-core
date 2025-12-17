# atlas/reasoning/stub.py

from typing import Dict, Any

from .base import ReasoningEngine


class StubReasoningEngine:
    """
    Temporary reasoning engine.
    """

    def generate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        user_text = context.get("user_text", "")

        return {
            "reply_text": f"ATLAS received your message: '{user_text}'",
            "confidence": 1.0,
            "model": "stub",
        }
