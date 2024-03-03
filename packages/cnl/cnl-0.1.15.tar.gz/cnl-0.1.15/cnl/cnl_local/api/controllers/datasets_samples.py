import json

from cnl_local.db.repositories.datasets_samples import get_dataset as get_dataset_
from cnl_local.db.repositories.datasets_samples import get_datasets as get_datasets_
from cnl_local.db.repositories.datasets_samples import get_sample as get_sample_
from cnl_local.db.repositories.datasets_samples import get_samples as get_samples_
from cnl_local.db.repositories.datasets_samples import get_samples_full
from cnl_local.db.repositories.datasets_samples import (
    update_or_create_dataset as update_or_create_dataset_,
)
from cnl_local.db.repositories.datasets_samples import (
    update_or_create_sample as update_or_create_sample_,
)
from cnl_local.types.datasets_samples.Dataset import Dataset
from cnl_local.types.datasets_samples.DatasetSample import DatasetSample
from fastapi import APIRouter, HTTPException, Response
from typing_extensions import List, Optional

router = APIRouter()


##
# Datasets
##
@router.get("/dataset", tags=["datasets_samples"])
def get_dataset(dataset_id: str) -> Optional[Dataset]:
    dataset = get_dataset_(dataset_id)
    if not dataset:
        raise HTTPException(status_code=404)
    return dataset


@router.get("/datasets", tags=["datasets_samples"])
def get_datasets() -> List[Dataset]:
    datasets = get_datasets_()
    return datasets


@router.post("/dataset", tags=["datasets_samples"])
def update_or_create_dataset(dataset: Dataset):
    update_or_create_dataset_(dataset)


@router.get("/download_dataset", tags=["datasets_samples"])
def download_dataset(dataset_id: str):
    samples = get_samples_full(dataset_id)
    response_content = "\n".join(
        [json.dumps({"messages": sample["messages"]}) for sample in samples]
    )
    headers = {
        "Content-Disposition": f"attachment; filename=cnl-dataset.jsonl",
        "Content-Type": "application/json",
    }
    return Response(content=response_content, headers=headers)


##
# Samples
##
@router.get("/sample", tags=["datasets_samples"])
def get_sample(dataset_id: str, sample_id: str) -> Optional[DatasetSample]:
    sample = get_sample_(dataset_id, sample_id)
    if not sample:
        raise HTTPException(status_code=404)
    return sample


@router.get("/samples", tags=["datasets_samples"])
def get_samples(dataset_id: str) -> List[DatasetSample]:
    samples = get_samples_(dataset_id)
    return samples


@router.post("/sample", tags=["datasets_samples"])
def update_or_create_sample(sample: DatasetSample):
    update_or_create_sample_(sample)
