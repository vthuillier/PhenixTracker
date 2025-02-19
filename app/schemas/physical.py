from datetime import date

from pydantic import BaseModel


class PhysicalAdd(BaseModel):
    weight: float
    height: float
    date: date
    arm_circumference: float
    waist_circumference: float
    hip_circumference: float
    thigh_circumference: float
    calf_circumference: float


class PhysicalOut(PhysicalAdd):
    id: int

    class Config:
        orm_mode = True


class PhysicalDelete(BaseModel):
    id: int
