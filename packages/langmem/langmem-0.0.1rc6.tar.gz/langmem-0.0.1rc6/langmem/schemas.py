from typing import Any, Dict
from typing_extensions import TypedDict


class GetThreadStateResponse(TypedDict, total=False):
    """
    Represents a response for a thread state.

    Attributes:
        state (Dict[str, Any]): The state of the thread.
    """

    state: Dict[str, Any]
