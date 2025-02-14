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
    OAUTH2_SCHEME: OAuth2PasswordBearer = OAuth2PasswordBearer(tokenUrl="token")
    SECRET_KEY: str | None = (
        os.getenv("SECRET_KEY") if os.getenv("SECRET_KEY") else "test"
    )
    ACCESS_TOKEN_EXPIRE_MINUTES: int = (
        int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))
        if os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")
        else 30
    )
    ALGORITHM: str = "HS256"
    SMTP_SERVER: str | None = os.getenv("SMTP_SERVER")
    SMTP_PORT: int | None = os.getenv("SMTP_PORT", 587)
    SMTP_TLS: bool = os.getenv("SMTP_TLS", True)
    SMTP_MAIL: str | None = os.getenv("SMTP_MAIL")
    SMTP_PASSWORD: str | None = os.getenv("SMTP_PASSWORD")
    WEB_URL: str = os.getenv("WEB_URL", "http://localhost:8000")


settings = Settings()
