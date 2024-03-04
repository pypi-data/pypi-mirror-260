from typing_extensions import Literal, TypedDict


class Event(TypedDict):
    type: Literal["user-message"]
    conversation_id: str
    message_id: str
    content: str
