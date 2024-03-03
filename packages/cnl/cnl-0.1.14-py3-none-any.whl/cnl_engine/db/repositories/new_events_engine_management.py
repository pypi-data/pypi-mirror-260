import json
import uuid

from typing_extensions import List, Literal, TypedDict

from cnl_engine.db.engine_session import SessionLocal
from cnl_engine.db.models.new_events_engine_management import NewEventsEngineManagement
from cnl_engine.types.common_types import BotMessageEvent, ConversationToRun, Event


def create_new_conversation(conversation_id: str):
    with SessionLocal() as session:
        new_row = NewEventsEngineManagement(
            conversation_id=conversation_id,
            new_events_for_front=json.dumps([]),
            engine_should_run=False,
            assigned_engine_id=None,
        )
        session.add(new_row)
        session.commit()


##
# Front back events
##
def add_event_for_front_from_engine_if_appropriate(
    conversation_id: str, engine_id: str, event: BotMessageEvent
) -> bool:
    """used by engine to send events to front
    returns whether was appropriate"""
    with SessionLocal() as session:
        row = (
            session.query(NewEventsEngineManagement)
            .filter(
                NewEventsEngineManagement.conversation_id == conversation_id,
                NewEventsEngineManagement.assigned_engine_id == engine_id,
            )
            .with_for_update()
            .first()
        )
        if not row:
            return False
        prev_events_for_front = json.loads(row.new_events_for_front)  # type: ignore
        row.new_events_for_front = json.dumps(prev_events_for_front + [event])  # type: ignore
        session.commit()
    return True


def add_event_for_front(conversation_id: str, event: BotMessageEvent):
    with SessionLocal() as session:
        row = (
            session.query(NewEventsEngineManagement)
            .filter(NewEventsEngineManagement.conversation_id == conversation_id)
            .with_for_update()
            .first()
        )
        prev_events_for_front = json.loads(row.new_events_for_front)  # type: ignore
        row.new_events_for_front = json.dumps(prev_events_for_front + [event])  # type: ignore
        session.commit()


def get_new_events_for_front(conversation_id: str) -> List[Event]:
    # get new events, reset list
    with SessionLocal() as session:
        row = (
            session.query(NewEventsEngineManagement)
            .filter(NewEventsEngineManagement.conversation_id == conversation_id)
            .first()
        )
        if row:
            new_events: List[Event] = json.loads(row.new_events_for_front)  # type: ignore
            row.new_events_for_front = json.dumps([])  # type: ignore
        else:
            new_events = []

        session.commit()
    return new_events


def register_events_from_front(conversation_id: str, events: List[Event]):
    pass


##
# Engine management
##
def get_conversations_to_run() -> List[ConversationToRun]:
    # get conversations to run, lock them
    # generate engine_ids for them
    # update table with engine_ids
    # return conversation_ids, engine_ids
    conversations_to_run: List[ConversationToRun] = []
    with SessionLocal() as session:
        rows = (
            session.query(NewEventsEngineManagement)
            .filter(
                NewEventsEngineManagement.engine_should_run == True,
            )
            .with_for_update()
            .all()
        )
        for row in rows:
            engine_id = str(uuid.uuid4())
            row.assigned_engine_id = engine_id  # type: ignore
            row.engine_should_run = False  # type: ignore
            conversations_to_run.append(
                {
                    "conversation_id": str(row.conversation_id),
                    "engine_id": engine_id,
                }
            )
        session.commit()

    return conversations_to_run


def set_engine_should_run(conversation_id: str):
    with SessionLocal() as session:
        row = (
            session.query(NewEventsEngineManagement)
            .filter(NewEventsEngineManagement.conversation_id == conversation_id)
            .with_for_update()
            .first()
        )
        if not row:
            row = NewEventsEngineManagement(
                conversation_id=conversation_id,
                new_events_for_front=json.dumps([]),
                engine_should_run=False,
                assigned_engine_id=None,
            )
            session.add(row)
        row.engine_should_run = True  # type: ignore
        session.commit()
