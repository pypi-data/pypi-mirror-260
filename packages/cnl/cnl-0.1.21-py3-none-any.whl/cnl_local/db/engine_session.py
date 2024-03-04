from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cnl_local.config import config

SQLALCHEMY_DATABASE_URL = config["db_connection_string"]

engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={
        "check_same_thread": False
    },  # needed for SQLite, remove for other databases
)

# Session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
