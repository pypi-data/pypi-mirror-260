import multiprocessing
import uuid
from multiprocessing.synchronize import Lock
from time import sleep

from cnl_deployment_targets.telegram.config import Config, config, set_config
from cnl_deployment_targets.telegram.operations.engine import (
    add_event,
    get_unread_events,
)
from cnl_deployment_targets.telegram.operations.tg import get_updates, send_message
from cnl_deployment_targets.telegram.types import ConversationTgChatMapping
from typing_extensions import List

# Remove lock from read operations


def _shared_conversation_repository_abuser(
    shared_conversation_repository: List[ConversationTgChatMapping],
    shared_conversation_repository_lock: Lock,
):
    while True:
        with shared_conversation_repository_lock:
            shared_conversation_repository_ = shared_conversation_repository[:]
            del shared_conversation_repository[:]
            shared_conversation_repository.extend(shared_conversation_repository_)
        sleep(0.01)


def new_events_from_tg_to_engine_relay(
    config_: Config,
    shared_conversation_repository: List[ConversationTgChatMapping],
    shared_conversation_repository_lock: Lock,
):
    set_config(config_)
    next_update_id = None
    while True:
        # get events from tg
        updates = get_updates(next_update_id)

        for update in updates:
            # check if tg chat id is present in list
            #   if not - create new conversation
            #   if yes - send to known coversation id
            # update that waiting for update
            tg_chat_id = update["message"]["chat"]["id"]
            with shared_conversation_repository_lock:
                conversation = next(
                    (
                        conversation
                        for conversation in shared_conversation_repository
                        if conversation["tg_chat_id"] == tg_chat_id
                    ),
                    None,
                )
            if not conversation:
                conversation_id = str(uuid.uuid4())
                with shared_conversation_repository_lock:
                    shared_conversation_repository.append(
                        {
                            "conversation_id": conversation_id,
                            "tg_chat_id": update["message"]["chat"]["id"],
                            "waiting_for_event_from_engine": False,
                        }
                    )
            else:
                conversation_id = conversation["conversation_id"]

            # add event to engine
            add_event(
                {
                    "message_id": str(uuid.uuid4()),
                    "conversation_id": conversation_id,
                    "type": "user-message",
                    "content": update["message"]["text"],
                }
            )

            # update conversation repository
            with shared_conversation_repository_lock:
                new_conversation_repository: List[ConversationTgChatMapping] = [
                    (
                        {**conversation, "waiting_for_event_from_engine": True}
                        if conversation["conversation_id"] == conversation_id
                        else conversation
                    )
                    for conversation in shared_conversation_repository
                ]
                shared_conversation_repository[:] = []  # Clear the list
                shared_conversation_repository.extend(new_conversation_repository)

            next_update_id = update["update_id"] + 1


def new_events_from_engine_to_tg_relay(
    config_: Config,
    shared_conversation_repository: List[ConversationTgChatMapping],
    shared_conversation_repository_lock: Lock,
):
    set_config(config_)
    while True:
        with shared_conversation_repository_lock:
            conversations_of_interest = [
                conversation
                for conversation in shared_conversation_repository
                if conversation["waiting_for_event_from_engine"] == True
            ]
        for conversation in conversations_of_interest:
            # get events from engine for conversation of interest
            events = get_unread_events(conversation["conversation_id"])
            if not events:
                continue
            # add events to tg
            for event in events:
                send_message(conversation["tg_chat_id"], event["content"])
            # update waiting_for_event_from_engine
            with shared_conversation_repository_lock:
                new_conversation_repository: List[ConversationTgChatMapping] = [
                    (
                        {**conversation_, "waiting_for_event_from_engine": False}
                        if conversation_["conversation_id"]
                        == conversation["conversation_id"]
                        else conversation_
                    )
                    for conversation_ in shared_conversation_repository
                ]
                shared_conversation_repository[:] = []  # Clear the list
                shared_conversation_repository.extend(new_conversation_repository)
        sleep(0.05)


def main(tg_api_key: str):
    set_config({**config, "tg_api_key": tg_api_key})  # type: ignore
    with multiprocessing.Manager() as manager:
        shared_conversation_repository = manager.list()
        shared_conversation_repository_lock = multiprocessing.Lock()

        # Start relays
        process = multiprocessing.Process(
            target=new_events_from_tg_to_engine_relay,
            args=(
                config,
                shared_conversation_repository,
                shared_conversation_repository_lock,
            ),
        )
        process.start()

        process = multiprocessing.Process(
            target=new_events_from_engine_to_tg_relay,
            args=(
                config,
                shared_conversation_repository,
                shared_conversation_repository_lock,
            ),
        )
        process.start()

        process.join()
