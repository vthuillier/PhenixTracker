from sqlalchemy import Column, Integer, ForeignKey, String, Date, Boolean
from sqlalchemy.orm import relationship

from app.db.session import Base


class ForgotPassword(Base):
    __tablename__ = "forgot_password"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    user = relationship("User", back_populates="forgot_password")
    token = Column(String, nullable=False, unique=True)
    expiration = Column(Date, nullable=False)
    used = Column(Boolean, nullable=False, default=False)
