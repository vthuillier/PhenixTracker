from sqlalchemy.orm import Session

from app.db.models.exercise import Exercise
from app.schemas.exercise import ExerciseCreate, ExerciseBase


def get_all_exercise(db: Session) -> list[ExerciseBase]:
    exercises = db.query(Exercise).all()
    return [ExerciseBase.model_validate(exercise) for exercise in exercises]


def get_exercise_by_id(db: Session, exercise_id: int) -> ExerciseBase:
    return ExerciseBase.model_validate(db.query(ExerciseBase).filter(Exercise.id == exercise_id).first())


def create_exercise(db: Session, exercise: ExerciseCreate) -> ExerciseBase:
    db_exercise = Exercise(**exercise.model_dump())
    db.add(db_exercise)
    db.commit()
    db.refresh(db_exercise)
    return ExerciseBase.model_validate(db_exercise)
