from typing import Type

from sqlalchemy.orm import Session

from app.db.models.physical import Physical
from app.schemas.physical import PhysicalAdd


def add_physical_data(
    db: Session, user_id: int, physical_data: PhysicalAdd
) -> Physical:
    db_physical = Physical(
        date=physical_data.date,
        height=physical_data.height,
        weight=physical_data.weight,
        user_id=user_id,
    )
    db.add(db_physical)
    db.commit()
    db.refresh(db_physical)
    return db_physical


def get_physical_data_by_id(db: Session, physical_id: int) -> Type[Physical] | None:
    return db.query(Physical).filter(Physical.id == physical_id).first()


def get_all_physical_data_for_user(db: Session, user_id: int) -> list[Type[Physical]]:
    return db.query(Physical).filter(Physical.user_id == user_id).all()


def update_physical_data(
    db: Session, physical_data: PhysicalAdd
) -> Type[Physical] | None:
    db_physical = get_physical_data_by_id(db, physical_data.id)
    db_physical.date = physical_data.date
    db_physical.height = physical_data.height
    db_physical.weight = physical_data.weight
    db.commit()
    db.refresh(db_physical)
    return db_physical


def delete_physical_data(db: Session, physical_data: Physical) -> Physical:
    db.delete(physical_data)
    db.commit()
    return physical_data
