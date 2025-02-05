from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.crud.user as crud
from app.core.security import get_current_user
from app.db.models.user import User
from app.dependencies import get_db
from app.schemas.user import UserCreate, UserMe, UserOut

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return crud.create_user(db=db, userCreate=user)


@router.get("/me", response_model=UserMe)
def read_users_me(current_user: User = Depends(get_current_user)) -> UserMe:
    """
    Endpoint protégé : retourne les infos de l'utilisateur connecté.
    """
    return UserMe(**current_user.__dict__)
