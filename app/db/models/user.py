import enum

from sqlalchemy import Column, Date, Integer, String, Enum
from sqlalchemy.orm import relationship

from app.db.session import Base


class RoleEnum(enum.Enum):
    USER = "user"
    ADMIN = "admin"


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    surname = Column(String, nullable=False)
    birthdate = Column(Date, nullable=False)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String, nullable=False)
    role = Column(Enum(RoleEnum), default=RoleEnum.USER, nullable=False)

    physical_data = relationship("Physical", back_populates="user", cascade="all, delete")
    forgot_password = relationship("ForgotPassword", back_populates="user", cascade="all, delete")
