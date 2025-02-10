import datetime

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import app.crud.physical as crud
from app.core.security import get_current_user
from app.db.models.user import User
from app.dependencies import get_db
from app.schemas.physical import PhysicalAdd, PhysicalOut, PhysicalDelete

router = APIRouter()


@router.get("/all")
def get_all_physical_data_for_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[PhysicalOut]:
    result = crud.get_all_physical_data_for_user(db, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="No physical data found")

    return [PhysicalOut(**item.__dict__) for item in result]


@router.get("/{physical_id}")
def get_physical_data_by_id(
        physical_id: int, db: Session = Depends(get_db)
) -> PhysicalOut:
    result = crud.get_physical_data_by_id(db, physical_id)

    if not result:
        raise HTTPException(status_code=404, detail="Physical data not found")

    return PhysicalOut(**result.__dict__)


@router.post("/add")
def add_physical_data(
    physical_data: PhysicalAdd,
    user: User = Depends(get_current_user),
    db: Session = Depends(get_db),
) -> PhysicalOut:
    result = crud.add_physical_data(db, user.id, physical_data)

    if not result:
        raise HTTPException(status_code=400, detail="Failed to add physical data")

    return PhysicalOut(**result.__dict__)


@router.delete("/delete")
def delete_physical_data(
        physical_data: PhysicalDelete,
        db: Session = Depends(get_db),
) -> None:
    if not crud.delete_physical_data(db, physical_data.id):
        raise HTTPException(status_code=400, detail="Failed to delete physical data")
    raise HTTPException(status_code=200, detail="Physical data deleted")


@router.get("/period")
def get_physical_data_by_period(
        start_date: str | None, end_date: str | None, db: Session = Depends(get_db),
        user: User = Depends(get_current_user)
) -> list[PhysicalOut]:
    if not start_date:
        start_date = (datetime.datetime.now(tz=datetime.timezone.utc).date() - datetime.timedelta(weeks=4)).strftime(
            "%Y-%m-%d")

    if not end_date:
        end_date = datetime.datetime.now(tz=datetime.timezone.utc).date().strftime("%Y-%m-%d")

    result = crud.get_physical_data_by_period(db, user.id, start_date, end_date)

    if not result:
        raise HTTPException(status_code=404, detail="No physical data found")

    return [PhysicalOut(**item.__dict__) for item in result]
