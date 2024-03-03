import uuid

from cnl_engine.db.repositories.conversation_history import get_history, update_history
from cnl_engine.db.repositories.new_events_engine_management import (
    set_engine_should_run,
)
from cnl_engine.services.conversation_history_manipulator import (
    update_conversation_history_with_new_message,
)
from cnl_engine.types.common_types import (
    ConversationHistoryMessage,
    Event,
    UserMessageEvent,
)
from cnl_engine.utils.utils import zulu_time_now_str


def handle_event_from_front(event: Event):
    if event["type"] == "user-message":
        handle_new_message_from_front_event(event)
    if event["type"] == "add-feedback":
        pass
    if event["type"] == "quick-reply":
        pass


def handle_new_message_from_front_event(event: UserMessageEvent):
    conversation_id = event["conversation_id"]

    # update history
    history = get_history(
        conversation_id=conversation_id
    )  # get history with repository

    new_conversation_history_message: ConversationHistoryMessage = {
        "message_id": str(uuid.uuid4()),
        "from_": "user",
        "content": event["content"],
        "dataset_samples": [],
        "feedback": "",
        "timestamp": zulu_time_now_str(),
    }
    history = update_conversation_history_with_new_message(
        history, new_conversation_history_message
    )

    update_history(conversation_id, history)

    # set engine should run
    set_engine_should_run(conversation_id)
