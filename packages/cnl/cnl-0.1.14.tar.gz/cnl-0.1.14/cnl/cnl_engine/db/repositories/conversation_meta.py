import json

from cnl_engine.db.engine_session import SessionLocal
from cnl_engine.db.models.conversation_meta import (
    ConversationMeta as ConversationMetaModel,
)


def get_meta(conversation_id: str) -> dict:
    with SessionLocal() as session:
        meta = (
            session.query(ConversationMetaModel)
            .filter(ConversationMetaModel.conversation_id == conversation_id)
            .first()
        )

    if meta:
        return json.loads(meta.meta_full)  # type: ignore

    # create if doesn't exist
    blank_meta = {}
    return blank_meta


def update_meta(conversation_id: str, new_meta: dict):
    with SessionLocal() as session:
        meta = (
            session.query(ConversationMetaModel)
            .filter(ConversationMetaModel.conversation_id == conversation_id)
            .first()
        )
        if meta:
            meta.meta_full = json.dumps(new_meta)  # type: ignore
            session.commit()
            return

        # create if doesn't exist
        meta = ConversationMetaModel(
            conversation_id=conversation_id, meta=json.dumps(new_meta)
        )
        session.add(meta)
        session.commit()
