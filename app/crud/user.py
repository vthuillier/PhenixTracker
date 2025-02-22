from sqlalchemy.orm import Session

from app.db.models.user import User, RoleEnum
from app.schemas.user import UserCreate
from app.services.auth import hash_password, verify_password


def create_user(db: Session, user_create: UserCreate, role: RoleEnum = RoleEnum.USER) -> User:
    hashed_password = hash_password(user_create.password)
    db_user = User(
        name=user_create.name,
        surname=user_create.surname,
        birthdate=user_create.birthdate,
        email=user_create.email,
        hashed_password=hashed_password,
        role=role
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user_by_id(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> User | None:
    return db.query(User).filter(User.email == email).first()


def reset_password(db: Session, default_password: str, new_password: str, user: User, force: bool = False) -> bool:
    if not verify_password(default_password, user.hashed_password) and not force:
        return False
    db_user = get_user_by_id(db, user.id)
    db_user.hashed_password = hash_password(new_password)
    db.commit()
    return True


def delete_user(db: Session, user: User) -> bool:
    db.delete(user)
    db.commit()
    return True
