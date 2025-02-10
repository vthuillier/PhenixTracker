from datetime import date

from pydantic import BaseModel


class PhysicalAdd(BaseModel):
    weight: float
    height: float
    date: date
    # TODO: Add somes fields to this table


class PhysicalOut(PhysicalAdd):
    id: int
    user_id: int

    class Config:
        orm_mode = True


class PhysicalUpdate(PhysicalAdd):
    pass


class PhysicalDelete(BaseModel):
    id: int


class PhysicalList(BaseModel):
    id: int
    date: date
    weight: float
    height: float
    user_id: int

    class Config:
        orm_mode = True
