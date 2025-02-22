from sqlalchemy import Integer, Column, String, LargeBinary, ForeignKey

from app.db.session import Base


class Exercise(Base):
    __tablename__ = "exercise"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, nullable=False)
    description = Column(String)
    picture = Column(LargeBinary)
    muscle_group_id = Column(Integer, ForeignKey("muscle.id"))
