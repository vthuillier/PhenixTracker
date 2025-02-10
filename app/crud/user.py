from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password


def create_user(db: Session, user_create: UserCreate):
    hashed_password = hash_password(user_create.password)
    db_user = User(
        name=user_create.name,
        surname=user_create.surname,
        birthdate=user_create.birthdate,
        email=user_create.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int):
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
