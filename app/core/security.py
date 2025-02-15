from datetime import datetime, timedelta
from typing import Optional

from fastapi import Depends, HTTPException, status
from jose import JWTError, jwt
from sqlalchemy.orm import Session

import app.crud.user as crud
from app.core.config import settings
from app.db.models.user import User, RoleEnum
from app.dependencies import get_db


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """
    Crée un token d'accès JWT.

    :param data: Données à inclure dans le token (ex: {"sub": user.email})
    :param expires_delta: Durée de validité du token
    :return: Token JWT encodé
    """
    to_encode = data.copy()
    expire = datetime.utcnow() + (
        expires_delta if expires_delta else timedelta(minutes=15)
    )
    to_encode.update({"exp": expire})

    encoded_jwt = jwt.encode(
        to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM
    )
    return encoded_jwt


def get_current_user(
    token: str = Depends(settings.OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> User:
    """
    Vérifie le token et retourne l'utilisateur authentifié.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = crud.get_user_by_email(db, email)
    if user is None:
        raise credentials_exception

    return user


def get_current_admin_user(
        token: str = Depends(settings.OAUTH2_SCHEME), db: Session = Depends(get_db)
) -> User | None:
    """
    Vérifie le token et retourne l'utilisateur authentifié s'il est admin.
    """
    user = get_current_user(token, db)
    if user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN, detail="User is not an admin"
        )
    return user
