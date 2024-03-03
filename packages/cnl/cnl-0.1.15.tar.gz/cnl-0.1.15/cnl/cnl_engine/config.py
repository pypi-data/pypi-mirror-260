import os

from typing_extensions import Literal, TypedDict

Env = Literal["dev", "prod"]

env: Env = os.environ.get("ENV", "dev").lower()  # type: ignore


class Config(TypedDict):
    # db
    db_connection_string: str
    # self api
    host: str
    port: int
    # conversation logging
    conversation_logging_host: str
    conversation_logging_port: int


dev_config: Config = {
    "db_connection_string": "sqlite:///./.cnl/engine-meta.db",
    "host": "0.0.0.0",
    "port": 5008,
    "conversation_logging_host": "localhost",
    "conversation_logging_port": 5009,
}

if env == "dev":
    config: Config = dev_config
