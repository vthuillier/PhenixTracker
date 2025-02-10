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


class PhysicalDelete(BaseModel):
    id: int
