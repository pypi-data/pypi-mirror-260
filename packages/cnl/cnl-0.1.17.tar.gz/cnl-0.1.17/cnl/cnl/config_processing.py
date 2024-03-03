# load config
# set up env vars

# repository of services and envvars

from cnl.types.Config import Config
from typing_extensions import NamedTuple, Optional, TypedDict, cast


def should_run_telegram(config: Config) -> bool:
    should_run_tg = False
    try:
        if config["telegram"]["api_key"]:
            should_run_tg = True
    except KeyError:
        pass
    return should_run_tg


class ConfigProcessingOutput(NamedTuple):
    should_run_telegram: bool
    telegram_config: Optional["TelegramConfig"]


class TelegramConfig(TypedDict):
    api_key: str
