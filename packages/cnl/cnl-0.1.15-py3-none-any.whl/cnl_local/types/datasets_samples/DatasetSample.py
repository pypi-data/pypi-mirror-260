from typing_extensions import List, TypedDict

from cnl_local.types.datasets_samples.SampleMessage import DatasetSampleMessage


class DatasetSample(TypedDict):
    dataset_id: str
    sample_id: str
    sample_name: str
    last_activity: str
    messages: List[DatasetSampleMessage]
