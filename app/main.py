from datetime import timedelta

from fastapi import Depends, FastAPI, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app.api.v1.endpoints import user
from app.core.config import settings
from app.core.security import create_access_token
from app.db.session import Base, engine
from app.dependencies import get_db
from app.schemas.token import Token
from app.services.auth import verify_password

Base.metadata.create_all(bind=engine)

app = FastAPI(title="PhenixTracker - API", version="0.0.1")

app.include_router(user.router, prefix="/users", tags=["Users"])


@app.get("/")
def read_root() -> dict[str, str]:
    """
    Root endpoint, just returns a simple message to the user
    :return:    (dict)  -   A simple message
    """
    return {"status": "ok"}


@app.post("/token", response_model=Token)
def get_token(
    form_data: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)
):
    """
    Endpoint to get a token
    :return:    (dict)  -   Access token and type
    """
    crud_user = user.crud.get_user_by_email(db, form_data.username)

    if not crud_user:
        raise HTTPException(status_code=400, detail="User not found")

    if not verify_password(form_data.password, crud_user.hashed_password):
        raise HTTPException(status_code=400, detail="Invalid password")

    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": crud_user.email}, expires_delta=access_token_expires
    )

    return {"access_token": access_token, "token_type": "bearer"}
