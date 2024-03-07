from sqlalchemy import Column, Integer, String, Float, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime

from sei_seeker_models.base import Base



class CollectionModel(Base):
    __tablename__ = 'collection'

    id = Column(Integer, primary_key=True)
    name = Column(String)
    contract_address = Column(String, unique=True)
    floor = Column(Float)
    volume = Column(Float)
    supply = Column(Integer)
    owners = Column(Integer)
    pfp = Column(String)
    twitter = Column(String)
    description = Column(String)
    banner = Column(String)
    discord = Column(String)
    created_at = Column(DateTime, default=datetime.utcnow)

    transactions = relationship("TransactionModel", back_populates="collection")
