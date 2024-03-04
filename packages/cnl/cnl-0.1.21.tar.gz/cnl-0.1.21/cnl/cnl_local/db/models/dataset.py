from sqlalchemy import Column, Integer, String

from ._base import Base


class Dataset(Base):
    __tablename__ = "datasets"

    dataset_id = Column(String, primary_key=True)
    dataset_full = Column(String)
