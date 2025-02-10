from typing import Type

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session

import app.crud.physical as crud
from app.core.security import get_current_user
from app.db.models.physical import Physical
from app.db.models.user import User
from app.dependencies import get_db
from app.schemas.physical import PhysicalAdd, PhysicalOut

router = APIRouter()


@router.get("/all")
def get_all_physical_data_for_user(
    user: User = Depends(get_current_user), db: Session = Depends(get_db)
) -> list[PhysicalOut]:
    result = crud.get_all_physical_data_for_user(db, user.id)

    if not result:
        raise HTTPException(status_code=404, detail="No physical data found")

    return [PhysicalOut(**item.__dict__) for item in result]


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
