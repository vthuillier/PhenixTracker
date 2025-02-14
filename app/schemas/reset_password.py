from pydantic import BaseModel


class ResetPassword(BaseModel):
    default_password: str
    new_password: str

    class Config:
        orm_mode = True


class ResetPasswordOut(BaseModel):
    confirmed: bool

    class Config:
        orm_mode = True
