import os

from typing_extensions import TypedDict


class Config(TypedDict):
    tg_api_key: str
    engine_url: str


global config
config: Config = {
    "tg_api_key": os.environ.get("CNL_TG_API_KEY", ""),
    "engine_url": "http://localhost:5008",
}


def set_config(new_config: Config):
    global config
    config = new_config


"""
-= ENV_VARS =-
--
CNL_TG_API_KEY

"""
