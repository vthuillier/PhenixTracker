from pydantic import BaseModel


class ExerciseBase(BaseModel):
    name: str
    description: str
    picture: bytes


class ExerciseCreate(ExerciseBase):
    pass


class ExerciseOut(ExerciseBase):
    id: int

    class Config:
        orm_mode = True
