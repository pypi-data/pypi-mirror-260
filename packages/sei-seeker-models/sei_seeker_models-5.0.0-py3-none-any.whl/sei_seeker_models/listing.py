from sqlalchemy import Column, String, Integer
from sei_seeker_models.base import Base


class ListingModel(Base):
    __tablename__ = 'listing'
    id = Column(Integer, primary_key=True, autoincrement=True)
    platform = Column(String)
    price = Column(String)
    address = Column(String)
    token_id = Column(String)
