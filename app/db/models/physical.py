from sqlalchemy import Column, Date, Double, ForeignKey, Integer
from sqlalchemy.orm import relationship

from app.db.session import Base


class Physical(Base):
    __tablename__ = "physical_data"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    date = Column(Date, nullable=False)
    height = Column(Double, nullable=True)
    weight = Column(Double, nullable=True)
    arm_circumference = Column(Double, nullable=True)
    waist_circumference = Column(Double, nullable=True)
    hip_circumference = Column(Double, nullable=True)
    thigh_circumference = Column(Double, nullable=True)
    calf_circumference = Column(Double, nullable=True)

    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="physical_data")
