from typing_extensions import List, TypedDict


class Config(TypedDict):
    # db
    db_connection_string: str


config: Config = {
    "db_connection_string": "sqlite:///./.cnl/cnl-local.db",
}
