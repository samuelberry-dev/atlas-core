# atlas/reasoning/base.py

from typing import Protocol, Dict, Any


class ReasoningEngine(Protocol):
    """
    Pure reasoning interface.

    Takes a prepared context and returns a response.

    """

    def generate(self, context: Dict[str, Any]) -> Dict[str, Any]:
        ...
