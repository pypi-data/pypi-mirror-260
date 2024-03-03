# cnl id
# cnl store

from sqlalchemy import UUID, Column, Integer, String

from ._base import Base


class CnlStore(Base):
    __tablename__ = "cnl_stores"

    store_id = Column(String, primary_key=True)
    store_full = Column(String)
