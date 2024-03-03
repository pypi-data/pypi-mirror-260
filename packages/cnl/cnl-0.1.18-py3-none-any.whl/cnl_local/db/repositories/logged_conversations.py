import json

from cnl_local.db.engine_session import SessionLocal
from cnl_local.db.models.logged_conversation import (
    LoggedConversation as LoggedConversationModel,
)
from cnl_local.types.logged_conversations import LoggedConversation
from cnl_local.utils.utils import zulu_time_now_str
from typing_extensions import List, Optional, cast


def get_logged_conversation(conversation_id: str) -> Optional[LoggedConversation]:
    with SessionLocal() as session:
        row = (
            session.query(LoggedConversationModel)
            .filter(LoggedConversationModel.conversation_id == conversation_id)
            .first()
        )
        if not row:
            return None
        conversation_full_str = cast(str, row.conversation_full)
    logged_conversation: LoggedConversation = json.loads(conversation_full_str)
    return logged_conversation


def get_logged_conversations() -> List[LoggedConversation]:
    with SessionLocal() as session:
        rows = session.query(LoggedConversationModel).all()
        conversation_short_strs = cast(
            List[str], [row.conversation_short for row in rows]
        )
    conversations_short: List[LoggedConversation] = [
        json.loads(conversation_short_str)
        for conversation_short_str in conversation_short_strs
    ]
    return conversations_short


def construct_logged_conversation_short(
    logged_conversation: LoggedConversation,
) -> LoggedConversation:
    logged_conversation_short: LoggedConversation = {
        "conversation_id": logged_conversation["conversation_id"],
        "last_activity": zulu_time_now_str(),
        "conversation_history": [],
    }
    return logged_conversation_short


def update_or_create_logged_conversation(logged_conversation: LoggedConversation):
    logged_conversation_short = json.dumps(
        construct_logged_conversation_short(logged_conversation)
    )
    logged_conversation_full = json.dumps(logged_conversation)
    with SessionLocal() as session:
        row = (
            session.query(LoggedConversationModel)
            .filter(
                LoggedConversationModel.conversation_id
                == logged_conversation["conversation_id"]
            )
            .first()
        )
        if row:
            row.conversation_short = logged_conversation_short  # type: ignore
            row.conversation_full = logged_conversation_full  # type: ignore
        else:
            new_row = LoggedConversationModel(
                conversation_id=logged_conversation["conversation_id"],
                conversation_short=logged_conversation_short,
                conversation_full=logged_conversation_full,
            )
            session.add(new_row)
        session.commit()
