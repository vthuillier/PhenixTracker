from typing import Type

from sqlalchemy.orm import Session

from app.db.models.physical import Physical
from app.schemas.physical import PhysicalAdd


def add_physical_data(
        db: Session, user_id: int, physical_data: PhysicalAdd
) -> Physical:
    db_physical = db.query(Physical).filter(
        Physical.user_id == user_id, Physical.date == physical_data.date
    ).first()

    if db_physical:
        db_physical.height = physical_data.height
        db_physical.weight = physical_data.weight
    else:
        db_physical = Physical(
            **physical_data.model_dump(), user_id=user_id
        )
        db.add(db_physical)

    db.commit()
    db.refresh(db_physical)
    return db_physical


def get_physical_data_by_id(db: Session, physical_id: int, user_id: int) -> Type[Physical] | None:
    return db.query(Physical).filter(Physical.id == physical_id, Physical.user_id == user_id).first()


def get_all_physical_data_for_user(db: Session, user_id: int) -> list[Type[Physical]]:
    return db.query(Physical).filter(Physical.user_id == user_id).all()


def update_physical_data(
        db: Session, physical_data: PhysicalAdd, user_id: int
) -> Type[Physical] | None:
    db_physical = get_physical_data_by_id(db, physical_data.id, user_id)
    if db_physical:
        db_physical.height = physical_data.height if physical_data.height else db_physical.height
        db_physical.weight = physical_data.weight if physical_data.weight else db_physical.weight
        db_physical.arm_circumference = physical_data.arm_circumference if physical_data.arm_circumference else db_physical.arm_circumference
        db_physical.waist_circumference = physical_data.waist_circumference if physical_data.waist_circumference else db_physical.waist_circumference
        db_physical.hip_circumference = physical_data.hip_circumference if physical_data.hip_circumference else db_physical.hip_circumference
        db_physical.thigh_circumference = physical_data.thigh_circumference if physical_data.thigh_circumference else db_physical.thigh_circumference
        db_physical.calf_circumference = physical_data.calf_circumference if physical_data.calf_circumference else db_physical.calf_circumference
    db.commit()
    db.refresh(db_physical)
    return db_physical


def delete_physical_data(db: Session, physical_data_id: int, user_id: int) -> bool:
    db_physical = get_physical_data_by_id(db, physical_data_id, user_id)
    if db_physical:
        db.delete(db_physical)
        db.commit()
        return True
    return False


def get_physical_data_by_period(db: Session, user_id: int, start_date: str, end_date: str):
    return (db.query(Physical)
            .filter(Physical.user_id == user_id, Physical.date >= start_date, Physical.date <= end_date)
            .order_by(Physical.date.asc())
            .all())
