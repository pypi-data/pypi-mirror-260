from sqlalchemy import Column, String, Integer, Float, ForeignKey
from sqlalchemy.orm import relationship
from sei_seeker_models.base import Base

class SnipeJobModel(Base):
    __tablename__ = 'snipe_job'
    id = Column(Integer, primary_key=True, autoincrement=True)
    price = Column(Float)
    status = Column(String)
    collection = Column(String)
    user_id = Column(Integer, ForeignKey('tg_user.id'))
    
    user = relationship("TgUserModel", back_populates="snipe_jobs")

