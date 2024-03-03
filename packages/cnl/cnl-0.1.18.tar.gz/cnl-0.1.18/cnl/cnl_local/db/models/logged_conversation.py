from sqlalchemy import Column, Integer, String

from ._base import Base


class LoggedConversation(Base):
    __tablename__ = "logged_conversations"

    conversation_id = Column(String, primary_key=True)
    conversation_short = Column(String)
    conversation_full = Column(String)
