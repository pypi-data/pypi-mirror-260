from sqlalchemy import UUID, Column, Integer, String

from ._base import Base


class ConversationMeta(Base):
    __tablename__ = "conversation_metas"

    conversation_id = Column(String, primary_key=True)
    meta_full = Column(String)
