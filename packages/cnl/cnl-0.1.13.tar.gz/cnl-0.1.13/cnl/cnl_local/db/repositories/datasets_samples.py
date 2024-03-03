import json

from cnl_local.db.engine_session import SessionLocal
from cnl_local.db.models.dataset import Dataset as DatasetModel
from cnl_local.db.models.sample import Sample as SampleModel
from cnl_local.types.datasets_samples.Dataset import Dataset
from cnl_local.types.datasets_samples.DatasetSample import DatasetSample
from typing_extensions import List, Optional, cast


##
# Datasets
##
def get_dataset(dataset_id: str) -> Optional[Dataset]:
    with SessionLocal() as session:
        row = (
            session.query(DatasetModel)
            .filter(DatasetModel.dataset_id == dataset_id)
            .first()
        )
        if not row:
            return None
        dataset_full_str = cast(str, row.dataset_full)
    dataset_full: Dataset = json.loads(dataset_full_str)
    return dataset_full


def get_datasets() -> List[Dataset]:
    with SessionLocal() as session:
        rows = session.query(DatasetModel).all()
        dataset_full_strs = cast(List[str], [row.dataset_full for row in rows])
    datasets_full: List[Dataset] = [
        json.loads(dataset_full_str) for dataset_full_str in dataset_full_strs
    ]
    return datasets_full


def construct_dataset(dataset: Dataset) -> Dataset:
    dataset_: Dataset = {
        "dataset_id": dataset["dataset_id"],
        "dataset_name": dataset["dataset_name"],
        "last_activity": dataset["last_activity"],
        "samples": [],
    }
    return dataset_


def update_or_create_dataset(dataset: Dataset):
    dataset_ = construct_dataset(dataset)
    with SessionLocal() as session:
        row = (
            session.query(DatasetModel)
            .filter(DatasetModel.dataset_id == dataset_["dataset_id"])
            .first()
        )
        if row:
            row.dataset_full = json.dumps(dataset_)  # type: ignore
        else:
            new_row = DatasetModel(
                dataset_id=dataset_["dataset_id"], dataset_full=json.dumps(dataset_)
            )
            session.add(new_row)
        session.commit()


##
# Samples
##
def get_sample(dataset_id: str, sample_id: str) -> Optional[DatasetSample]:
    with SessionLocal() as session:
        row = (
            session.query(SampleModel)
            .filter(SampleModel.dataset_id == dataset_id)
            .filter(SampleModel.sample_id == sample_id)
            .first()
        )
        if not row:
            return None
        sample_full_str = cast(str, row.sample_full)
    sample_full: DatasetSample = json.loads(sample_full_str)
    return sample_full


def get_samples(dataset_id: str) -> List[DatasetSample]:
    with SessionLocal() as session:
        rows = (
            session.query(SampleModel)
            .filter(SampleModel.dataset_id == dataset_id)
            .all()
        )
        sample_short_strs = cast(List[str], [row.sample_short for row in rows])
    samples_short: List[DatasetSample] = [
        json.loads(sample_short_str) for sample_short_str in sample_short_strs
    ]
    return samples_short


def get_samples_full(dataset_id: str) -> List[DatasetSample]:
    with SessionLocal() as session:
        rows = (
            session.query(SampleModel)
            .filter(SampleModel.dataset_id == dataset_id)
            .all()
        )
        sample_full_strs = cast(List[str], [row.sample_full for row in rows])
    samples_full: List[DatasetSample] = [
        json.loads(sample_full_str) for sample_full_str in sample_full_strs
    ]
    return samples_full


def construct_sample_short(sample: DatasetSample) -> DatasetSample:
    sample_short: DatasetSample = {
        "dataset_id": sample["dataset_id"],
        "sample_id": sample["sample_id"],
        "sample_name": sample["sample_name"],
        "last_activity": sample["last_activity"],
        "messages": [],
    }
    return sample_short


def update_or_create_sample(sample: DatasetSample):
    sample_short = json.dumps(construct_sample_short(sample))
    sample_full = json.dumps(sample)
    with SessionLocal() as session:
        row = (
            session.query(SampleModel)
            .filter(SampleModel.dataset_id == sample["dataset_id"])
            .filter(SampleModel.sample_id == sample["sample_id"])
            .first()
        )
        if row:
            row.sample_short = sample_short  # type: ignore
            row.sample_full = sample_full  # type: ignore
        else:
            new_row = SampleModel(
                dataset_id=sample["dataset_id"],
                sample_id=sample["sample_id"],
                sample_short=sample_short,
                sample_full=sample_full,
            )
            session.add(new_row)
        session.commit()
