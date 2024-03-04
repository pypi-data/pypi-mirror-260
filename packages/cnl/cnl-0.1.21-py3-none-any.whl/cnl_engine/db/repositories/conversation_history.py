import json

from cnl_engine.db.engine_session import SessionLocal
from cnl_engine.db.models.conversation_history import (
    ConversationHistory as ConversationHistoryModel,
)
from cnl_engine.types.common_types import ConversationHistory


def get_history(conversation_id: str) -> ConversationHistory:
    with SessionLocal() as session:
        conversation_history = (
            session.query(ConversationHistoryModel)
            .filter(ConversationHistoryModel.conversation_id == conversation_id)
            .first()
        )

    if conversation_history:
        return json.loads(conversation_history.history)  # type: ignore

    # create if doesn't exist
    blank_conversation_history: ConversationHistory = []
    return blank_conversation_history


def update_history(conversation_id: str, new_history: ConversationHistory):
    with SessionLocal() as session:
        conversation_history = (
            session.query(ConversationHistoryModel)
            .filter(ConversationHistoryModel.conversation_id == conversation_id)
            .first()
        )
        if conversation_history:
            conversation_history.history = json.dumps(new_history)  # type: ignore
            session.commit()
            return

        # create if doesn't exist
        conversation_history = ConversationHistoryModel(
            conversation_id=conversation_id, history=json.dumps(new_history)
        )
        session.add(conversation_history)
        session.commit()
