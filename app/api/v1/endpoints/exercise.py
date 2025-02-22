from typing import Type

from fastapi import APIRouter, HTTPException
from fastapi.params import Depends
from sqlalchemy.orm import Session
from starlette import status

from app.core.security import get_current_user, get_current_admin_user
from app.db.models.user import User, RoleEnum
from app.dependencies import get_db

import app.crud.exercise as crud
from app.schemas.exercise import ExerciseCreate, ExerciseOut, ExerciseBase

router = APIRouter()


@router.get("/", response_model=list[Type[ExerciseOut]])
def get_all_exercise(
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    all_exercises = crud.get_all_exercise(db)
    return [ExerciseOut.model_validate(exercise) for exercise in all_exercises]


@router.get("/{exercise_id}", response_model=Type[ExerciseBase])
def get_exercise_by_id(
        exercise_id: int,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    return crud.get_exercise_by_id(db, exercise_id)


@router.post("/", response_model=Type[ExerciseBase])
def create_exercise(
        exercise: ExerciseCreate,
        user: User = Depends(get_current_user),
        db: Session = Depends(get_db)
):
    if user.role != RoleEnum.COACH and user.role != RoleEnum.ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Vous n'avez pas les droits pour créer un exercice."
        )
    return crud.create_exercise(db, exercise)
