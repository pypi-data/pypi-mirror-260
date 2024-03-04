from sqlalchemy import UUID, Column, Integer, String

from ._base import Base


class ConversationHistory(Base):
    __tablename__ = "conversation_histories"

    conversation_id = Column(String, primary_key=True)
    history = Column(String)
