import json

from cnl_engine.db.engine_session import SessionLocal
from cnl_engine.db.models.cnl_store import CnlStore as CnlStoreModel


def get_store(store_id: str) -> dict:
    with SessionLocal() as session:
        store = (
            session.query(CnlStoreModel)
            .filter(CnlStoreModel.store_id == store_id)
            .first()
        )

    if store:
        return json.loads(store.store_full)  # type: ignore

    # create if doesn't exist
    blank_store = {}
    return blank_store


def update_store(store_id: str, new_store: dict):
    with SessionLocal() as session:
        store = (
            session.query(CnlStoreModel)
            .filter(CnlStoreModel.store_id == store_id)
            .first()
        )
        if store:
            store.store_full = json.dumps(new_store)  # type: ignore
            session.commit()
            return

        # create if doesn't exist
        store = CnlStoreModel(store_id=store_id, store_full=json.dumps(new_store))
        session.add(store)
        session.commit()
