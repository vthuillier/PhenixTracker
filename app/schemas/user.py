from datetime import date

from pydantic import BaseModel


class UserCreate(BaseModel):
    name: str
    surname: str
    email: str
    birthdate: date
    password: str


class UserLogin(BaseModel):
    email: str
    password: str


class UserOut(BaseModel):
    id: int

    class Config:
        orm_mode = True


class UserMe(UserOut):
    email: str
    name: str
    surname: str
    birthdate: date

    class Config:
        orm_mode = True
