from typing_extensions import TypedDict


class Config(TypedDict):
    # user config (user facing)
    telegram: "TelegramConfig"


class TelegramConfig(TypedDict):
    api_key: str
