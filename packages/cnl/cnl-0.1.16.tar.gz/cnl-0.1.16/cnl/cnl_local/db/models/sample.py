from sqlalchemy import Column, Integer, String

from ._base import Base


class Sample(Base):
    __tablename__ = "samples"

    dataset_id = Column(String)
    sample_id = Column(String, primary_key=True)
    sample_short = Column(String)
    sample_full = Column(String)
