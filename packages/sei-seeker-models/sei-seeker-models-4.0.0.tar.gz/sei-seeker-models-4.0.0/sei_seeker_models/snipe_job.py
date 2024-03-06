from sqlalchemy import Column, String, Integer, Float
from sei_seeker_models.base import Base


class SnipeJobModel(Base):
    __tablename__ = 'snipe_job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    key = Column(String)
    price = Column(Float)
    status = Column(String)
    collection = Column(String)
    user_id = Column(String)

