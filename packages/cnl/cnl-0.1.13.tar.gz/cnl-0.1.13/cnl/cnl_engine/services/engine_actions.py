"Actions that engine can take to modify conversation state (in db)"
import uuid

from cnl_engine.db.repositories.conversation_history import get_history, update_history
from cnl_engine.db.repositories.new_events_engine_management import (
    add_event_for_front,
    add_event_for_front_from_engine_if_appropriate,
)
from cnl_engine.services.conversation_history_manipulator import (
    update_conversation_history_with_data_sample,
    update_conversation_history_with_new_message,
)
from cnl_engine.types.common_types import (
    BotMessageEvent,
    ChatMessage,
    ConversationHistoryMessage,
    UserMessageEvent,
)
from cnl_engine.utils.utils import zulu_time_now_str


def send_message_if_appropriate(
    conversation_id: str, engine_id: str, message: ChatMessage
):
    message_id = str(uuid.uuid4())
    now = zulu_time_now_str()
    event_for_front: BotMessageEvent = {
        "type": "bot-message",
        "conversation_id": conversation_id,
        "message_id": message_id,
        "content": message["content"],
    }
    was_appropriate = add_event_for_front_from_engine_if_appropriate(
        conversation_id=conversation_id, engine_id=engine_id, event=event_for_front
    )

    # update history
    if was_appropriate:
        history = get_history(conversation_id=conversation_id)

        new_conversation_history_message: ConversationHistoryMessage = {
            "message_id": message_id,
            "from_": "bot",
            "content": message["content"],
            "dataset_samples": [],
            "feedback": "",
            "timestamp": now,
        }
        history = update_conversation_history_with_new_message(
            history, new_conversation_history_message
        )

        for data_sample in message["dataset_samples"]:
            history = update_conversation_history_with_data_sample(
                history, message_id, data_sample
            )

        update_history(conversation_id, history)


def force_send_message(conversation_id: str, message: ChatMessage):
    message_id = str(uuid.uuid4())
    now = zulu_time_now_str()
    event_for_front: BotMessageEvent = {
        "type": "bot-message",
        "conversation_id": conversation_id,
        "message_id": message_id,
        "content": message["content"],
    }
    add_event_for_front(conversation_id=conversation_id, event=event_for_front)

    # update history
    history = get_history(conversation_id=conversation_id)

    new_conversation_history_message: ConversationHistoryMessage = {
        "message_id": message_id,
        "from_": "bot",
        "content": message["content"],
        "dataset_samples": [],
        "feedback": "",
        "timestamp": now,
    }
    history = update_conversation_history_with_new_message(
        history, new_conversation_history_message
    )

    for data_sample in message["dataset_samples"]:
        history = update_conversation_history_with_data_sample(
            history, message_id, data_sample
        )

    update_history(conversation_id, history)


def send_typing_animation(conversation_id: str, engine_id: str):
    pass
