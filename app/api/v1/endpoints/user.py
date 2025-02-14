from datetime import datetime

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

import app.crud.forgot_password as crud_forgot_password
import app.crud.user as crud
from app.core.security import get_current_user
from app.db.models.user import User
from app.dependencies import get_db
from app.schemas.forgot_password import ForgotPassword, ForgotPasswordReset, ForgotPasswordResetOut
from app.schemas.reset_password import ResetPasswordOut, ResetPassword
from app.schemas.user import UserCreate, UserMe, UserOut
from app.services.mail import Mailer

router = APIRouter()


@router.post("/register", response_model=UserOut)
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = crud.get_user_by_email(db, user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="User already registered")

    return crud.create_user(db=db, user_create=user)


@router.get("/me", response_model=UserMe)
def read_users_me(current_user: User = Depends(get_current_user)) -> UserMe:
    """
    Endpoint protégé : retourne les infos de l'utilisateur connecté.
    """
    return UserMe(**current_user.__dict__)


@router.patch("/password", response_model=ResetPasswordOut)
def reset_password(
        reset_password: ResetPassword,
        db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
) -> ResetPasswordOut:
    """
    Endpoint protégé : permet à l'utilisateur de changer son mot de passe.
    """
    return ResetPasswordOut(
        confirmed=crud.reset_password(
            db,
            reset_password.default_password,
            reset_password.new_password,
            user
        )
    )


@router.get("/forgot-password")
def forgot_password(forgot_password: ForgotPassword, db: Session = Depends(get_db)) -> None:
    """
    Endpoint public : envoie un email de réinitialisation de mot de passe.
    """
    email = forgot_password.email

    if not crud.get_user_by_email(db, email):
        raise HTTPException(status_code=404, detail="User not found")

    forgot_password = crud_forgot_password.add_forgot_password(db, email)

    if not forgot_password:
        raise HTTPException(status_code=500,
                            detail="An error occurred, please contact the administrator to force reset your password")

    try:
        mailer = Mailer()
        with open("app/templates/forgot_password.html") as file:
            mailer.send_mail(email, "[PhenixTracker] Réinitialisation de votre mot de passe",
                             file.read().replace("{{ token }}", forgot_password.token))
    except ValueError:
        raise HTTPException(status_code=500,
                            detail="Mail not sent, please contact the administrator to force reset your password")
    except FileNotFoundError:
        raise HTTPException(status_code=500,
                            detail="Template not found, please contact the administrator to force reset your password")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/forgot-password", response_model=ForgotPasswordResetOut)
def reset_password(forgot: ForgotPasswordReset, db: Session = Depends(get_db)) -> ForgotPasswordResetOut:
    """
    Endpoint public : permet à l'utilisateur de réinitialiser son mot de passe.
    """
    forgot_password = crud_forgot_password.get_forgot_password(db, forgot.token)

    if not forgot_password:
        raise HTTPException(status_code=404, detail="Token not found")

    if forgot_password.used:
        raise HTTPException(status_code=400, detail="Token already used")

    if forgot_password.expiration >= datetime.now():
        raise HTTPException(status_code=400, detail="Token expired")

    user = crud.get_user_by_id(db, forgot_password.user_id)

    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    crud.reset_password(db, "", forgot.new_password, user, force=True)
    forgot_password.used = True
    db.commit()

    return ForgotPasswordResetOut(confirmed=True)
