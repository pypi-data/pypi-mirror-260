from cnl_engine.db.engine_session import engine
from cnl_engine.db.models._base import Base  # Import base
from cnl_engine.db.models.cnl_store import CnlStore
from cnl_engine.db.models.conversation_history import ConversationHistory
from cnl_engine.db.models.conversation_meta import ConversationMeta
from cnl_engine.db.models.new_events_engine_management import NewEventsEngineManagement


def create_tables():
    Base.metadata.drop_all(engine)
    # Importing the models is essential for create_all to recognize them
    Base.metadata.create_all(engine)


if __name__ == "__main__":
    create_tables()
