from typing_extensions import TypedDict


class ConversationTgChatMapping(TypedDict):
    tg_chat_id: int
    conversation_id: str
    waiting_for_event_from_engine: bool
