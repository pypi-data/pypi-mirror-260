import multiprocessing
from time import sleep

from cnl_deployment_targets.telegram.config import Config
from cnl_deployment_targets.telegram.config import config as config_
from cnl_deployment_targets.telegram.main import (
    _shared_conversation_repository_abuser,
    new_events_from_engine_to_tg_relay,
    new_events_from_tg_to_engine_relay,
)

config: Config = {
    **config_,
    "tg_api_key": "6595909512:AAGvjv3m_g9sB3oZovrkVhq4bTOvV_wQSZA",
}


def main():
    with multiprocessing.Manager() as manager:
        shared_conversation_repository = manager.list()
        shared_conversation_repository_lock = multiprocessing.Lock()

        process = multiprocessing.Process(
            target=_shared_conversation_repository_abuser,
            args=(
                shared_conversation_repository,  # type: ignore
                shared_conversation_repository_lock,
            ),
        )
        process.start()

        process = multiprocessing.Process(
            target=new_events_from_tg_to_engine_relay,
            args=(
                config,
                shared_conversation_repository,  # type: ignore
                shared_conversation_repository_lock,
            ),
        )
        process.start()

        # this one as well
        process = multiprocessing.Process(
            target=new_events_from_engine_to_tg_relay,
            args=(
                config,
                shared_conversation_repository,  # type: ignore
                shared_conversation_repository_lock,
            ),
        )
        process.start()

        process.join()


if __name__ == "__main__":
    main()
