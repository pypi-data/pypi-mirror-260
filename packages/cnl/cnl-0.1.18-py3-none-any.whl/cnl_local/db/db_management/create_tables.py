import uuid

from cnl_local.db.engine_session import engine
from cnl_local.db.models._base import Base  # Import base
from cnl_local.db.models.dataset import Dataset  # Import all models
from cnl_local.db.models.sample import Sample
from cnl_local.db.repositories.datasets_samples import (
    get_datasets,
    update_or_create_dataset,
)


def create_tables():
    # Base.metadata.drop_all(engine)

    # Importing the models is essential for create_all to recognize them
    Base.metadata.create_all(engine)

    populate_if_empty()


def populate_if_empty():
    datasets = get_datasets()
    if not datasets:
        update_or_create_dataset(
            {
                "dataset_id": str(uuid.uuid4()),
                "dataset_name": "Default dataset",
                "last_activity": "",
                "samples": [],
            }
        )
