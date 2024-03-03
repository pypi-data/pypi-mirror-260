from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from cnl_engine.config import config

engine = create_engine(
    config["db_connection_string"],
    connect_args={
        "check_same_thread": False,  # needed for SQLite, remove for other databases
    },
    # echo=True,
)

# Create a session factory
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
