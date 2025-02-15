import os
from datetime import timedelta, datetime

from sqlalchemy.orm import Session

import app.crud.user as crud_user
from app.db.models.forgot_password import ForgotPassword
from app.db.models.user import User


def get_forgot_password(db: Session, token: str) -> ForgotPassword | None:
    """
    Récupère une demande de réinitialisation de mot de passe par son token.
    """
    return db.query(ForgotPassword).filter(ForgotPassword.token == token).first()


def get_forgotten_password_by_user_id(db: Session, user_id: int) -> ForgotPassword | None:
    """
    Récupère une demande de réinitialisation de mot de passe par l'ID de l'utilisateur.
    """
    return db.query(ForgotPassword).filter(ForgotPassword.user_id == user_id).first()


def add_forgot_password(db: Session, email: str) -> ForgotPassword | None:
    """
    Ajoute une demande de réinitialisation de mot de passe à la base de données.
    """
    user: User | None = crud_user.get_user_by_email(db, email)

    if not user:
        return None

    if forgotten_password := get_forgotten_password_by_user_id(db, user.id):
        db.delete(forgotten_password)
        db.commit()

    token = os.urandom(128).hex()

    forgot_password = ForgotPassword(
        user_id=user.id,
        token=token,
        expiration=datetime.now() + timedelta(days=1)
    )

    db.add(forgot_password)
    db.commit()
    db.refresh(forgot_password)
    return forgot_password
