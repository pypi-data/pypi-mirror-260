from typing_extensions import Optional, TypedDict


class Update(TypedDict):
    update_id: int
    message: "Message"


class Message(TypedDict):
    message_id: int
    chat: "Chat"
    date: int
    text: str


class Chat(TypedDict):
    id: int
    # username: str
    # first_name: str
    # last_name: str
