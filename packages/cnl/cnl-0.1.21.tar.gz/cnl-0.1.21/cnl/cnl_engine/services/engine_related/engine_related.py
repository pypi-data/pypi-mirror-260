import threading
import uuid
from multiprocessing import Pool
from pprint import pprint
from time import sleep

import httpx
from cnl_engine.config import config
from cnl_engine.db.repositories.conversation_history import get_history
from cnl_engine.db.repositories.new_events_engine_management import (
    get_conversations_to_run,
)
from cnl_engine.services.engine_actions import (
    force_send_message,
    send_message_if_appropriate,
)
from cnl_engine.services.engine_related.user_function_process_wrapper import (
    user_function_process_wrapper,
)
from cnl_engine.types.common_types import (
    ChatMessage,
    EnginesManagerEngineMeta,
    LoggedConversation,
)
from cnl_engine.utils.utils import zulu_time_now_str
from typing_extensions import Dict, List, Optional


class EnginesManager:
    def __init__(self, path_to_user_function: Optional[str]):
        self.engines_metas: List[EnginesManagerEngineMeta] = []
        self.engines: Dict[str, Engine] = {}
        self.path_to_user_function: str = path_to_user_function or (
            "get default function from package files or just from nearby"
        )

    def periodic_task(self):
        # get rows for engines that need to run from db
        conversations_to_run = get_conversations_to_run()
        # create engine, run it, save its reference in engines mapping
        for conversation_to_run in conversations_to_run:
            engine = Engine(
                conversation_to_run["conversation_id"],
                conversation_to_run["engine_id"],
                self.path_to_user_function,
            )
            self.engines[conversation_to_run["conversation_id"]] = engine
            engine.start_in_thread()
        pass

    def run_periodic_task(self):
        while True:
            self.periodic_task()
            sleep(0.05)


class Engine:
    def __init__(
        self,
        conversation_id: str,
        engine_id: str,
        path_to_user_function_file: str,
    ):
        self.conversation_id = conversation_id
        self.engine_id = engine_id
        self.path_to_user_function_file = path_to_user_function_file
        self.thread = None

    def user_function_thread_wrapper(self):
        "what will be run in thread"
        with Pool(processes=1) as pool:
            result_async = pool.apply_async(
                user_function_process_wrapper,
                args=(
                    self.path_to_user_function_file,
                    self.conversation_id,
                    self.conversation_id,
                ),
            )
            result: ChatMessage = result_async.get()
        # send_message_if_appropriate(self.conversation_id, self.engine_id, result)
        force_send_message(self.conversation_id, result)

        # log conversation
        # get conversation, log to cnl local
        history = get_history(self.conversation_id)
        new_logged_conversation: LoggedConversation = {
            "conversation_id": self.conversation_id,
            "last_activity": zulu_time_now_str(),
            "conversation_history": history,
        }
        # print(f"Going to log:")
        # pprint(new_logged_conversation)
        httpx.post(
            f'http://{config["conversation_logging_host"]}:{config["conversation_logging_port"]}/log_conversation',
            json=new_logged_conversation,
        )

    def start_in_thread(self):
        self.thread = threading.Thread(
            target=self.user_function_thread_wrapper,  # args=(self,)
        )
        self.thread.start()

    def get_greeting(self) -> str:
        return "this is greeting"
