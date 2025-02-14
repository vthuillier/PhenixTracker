from sqlalchemy import Column, Date, Integer, String
from sqlalchemy.orm import relationship

from app.db.session import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)

    physical_data = relationship("Physical", back_populates="user")
    forgot_password = relationship("ForgotPassword", back_populates="user")
