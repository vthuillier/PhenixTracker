from pydantic import BaseModel


class ForgotPassword(BaseModel):
    email: str

    class Config:
        orm_mode = True


class ForgotPasswordReset(BaseModel):
    token: str
    new_password: str

    class Config:
        orm_mode = True


class ForgotPasswordResetOut(BaseModel):
    confirmed: bool

    class Config:
        orm_mode = True
