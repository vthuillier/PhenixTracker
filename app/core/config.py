import os

from dotenv import load_dotenv
from fastapi.security import OAuth2PasswordBearer

load_dotenv()


class Settings:
    DATABASE_URL: str | None = (
        os.getenv("DATABASE_URL")
        if os.getenv("DATABASE_URL")
        else "sqlite:///./test.db"
    )
    OAUTH2_SCHEME = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY: str | None = (
        os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else "test"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES = (
        int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        if os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        else 30
    )
    ALGORITHM = "HS256"


settings = Settings()
