import uuid
from pprint import pprint

from cnl_engine.api.schemas import CreatedConversationId
from cnl_engine.db.repositories.new_events_engine_management import (
    create_new_conversation,
    get_new_events_for_front,
)
from cnl_engine.services.events_from_front_handler import handle_event_from_front
from cnl_engine.types.common_types import Event
from fastapi import APIRouter

router = APIRouter()


# @router.post("/create-conversation")
# def create_conversation() -> CreatedConversationId:
#     conversation_id = str(uuid.uuid4())
#     create_new_conversation(conversation_id)
#     return {"conversation_id": conversation_id}


@router.post("/add_event")
def add_event(event: Event):
    handle_event_from_front(event)


@router.get("/get_unread_for_front")
def get_new_events(conversation_id: str):
    return get_new_events_for_front(conversation_id)


# /get-greeting
def get_greeting(conversation_id: str):
    pass
