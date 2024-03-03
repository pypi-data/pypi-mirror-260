from sqlalchemy import UUID, Boolean, Column, Integer, String

from ._base import Base


class NewEventsEngineManagement(Base):
    __tablename__ = "new_events_engine_management"

    conversation_id = Column(String, primary_key=True)
    # there_are_new_events_for_front = Column(Boolean)
    new_events_for_front = Column(String)
    engine_should_run = Column(Boolean)
    assigned_engine_id = Column(String, nullable=True)
    # engine_expects_new_event = Column(Boolean)
    # there_are_new_events_for_back = Column(Boolean)
    # new_events_for_back = Column(String)
