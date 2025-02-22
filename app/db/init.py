import datetime
import os

from sqlalchemy.orm import Session

from app.db.models.user import RoleEnum
from app.schemas.user import UserCreate

import app.crud.user as crud


def init_db(db: Session) -> None:
    admin_user = os.environ.get("ADMIN_USER", "admin")
    admin_password = os.environ.get("ADMIN_PASSWORD", "admin")
    admin_mail = os.environ.get("ADMIN_MAIL", "admin@admin.admin")
    admin_birthday = datetime.date.fromisocalendar(1999, 1, 1)
    admin = UserCreate(
        name=admin_user,
        surname=admin_user,
        birthdate=admin_birthday,
        email=admin_mail,
        password=admin_password,
    )
    crud.create_user(db, admin, role=RoleEnum.ADMIN)
    return True