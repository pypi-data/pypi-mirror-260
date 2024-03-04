from typing_extensions import List, TypedDict

from cnl_local.types.datasets_samples.DatasetSample import DatasetSample


class Dataset(TypedDict):
    dataset_id: str
    dataset_name: str
    last_activity: str
    samples: List[DatasetSample]
