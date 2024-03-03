from typing_extensions import TypedDict

from cnl_local.types.datasets_samples.Role import Role


class DatasetSampleMessage(TypedDict):
    role: Role
    content: str
