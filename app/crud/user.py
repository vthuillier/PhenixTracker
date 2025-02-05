from sqlalchemy.orm import Session

from app.db.models.user import User
from app.schemas.user import UserCreate
from app.services.auth import hash_password


def create_user(db: Session, userCreate: UserCreate):
    hashed_password = hash_password(userCreate.password)
    db_user = User(
        name=userCreate.name,
        surname=userCreate.surname,
        birthdate=userCreate.birthdate,
        email=userCreate.email,
        hashed_password=hashed_password,
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, id: int):
    return db.query(User).filter(User.id == id).first()


def get_user_by_email(db: Session, email: str):
    return db.query(User).filter(User.email == email).first()
