from sqlalchemy import Column, String, LargeBinary, Integer

from app.db.session import Base


class Muscle(Base):
    __tablename__ = "muscle"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=True)
    picture = Column(LargeBinary, nullable=True)
