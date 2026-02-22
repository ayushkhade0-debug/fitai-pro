from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database.db import get_db
from database import db as db_models
from database.auth import get_current_user
from models.schemas import WorkoutLogRequest, WorkoutLogResponse

router = APIRouter(prefix="/workouts", tags=["Workout History"])

@router.post("/log", response_model=WorkoutLogResponse)
def log_workout(data: WorkoutLogRequest,
                current_user: db_models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """Log a completed workout session."""
    entry = db_models.WorkoutHistory(
        user_id=current_user.id,
        exercise=data.exercise,
        duration=data.duration,
        calories=data.calories,
        sets=data.sets,
        reps=data.reps,
        notes=data.notes,
    )
    db.add(entry)
    db.commit()
    db.refresh(entry)
    return entry

@router.get("/history", response_model=List[WorkoutLogResponse])
def get_history(limit: int = 20,
                current_user: db_models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    """Get workout history for current user."""
    workouts = db.query(db_models.WorkoutHistory).filter(
        db_models.WorkoutHistory.user_id == current_user.id
    ).order_by(db_models.WorkoutHistory.logged_at.desc()).limit(limit).all()
    return workouts

@router.get("/stats")
def get_stats(current_user: db_models.User = Depends(get_current_user),
              db: Session = Depends(get_db)):
    """Get summary stats for current user's workouts."""
    workouts = db.query(db_models.WorkoutHistory).filter(
        db_models.WorkoutHistory.user_id == current_user.id
    ).all()

    if not workouts:
        return {"total_sessions": 0, "total_calories": 0,
                "total_minutes": 0, "favourite_exercise": "None"}

    total_cal  = round(sum(w.calories for w in workouts), 1)
    total_mins = sum(w.duration for w in workouts)

    # Find favourite exercise
    from collections import Counter
    fav = Counter(w.exercise for w in workouts).most_common(1)[0][0]

    return {
        "total_sessions":    len(workouts),
        "total_calories":    total_cal,
        "total_minutes":     total_mins,
        "favourite_exercise": fav,
        "avg_calories_per_session": round(total_cal / len(workouts), 1),
        "avg_duration":      round(total_mins / len(workouts), 1),
    }

@router.delete("/delete/{workout_id}")
def delete_workout(workout_id: int,
                   current_user: db_models.User = Depends(get_current_user),
                   db: Session = Depends(get_db)):
    """Delete a specific workout log entry."""
    entry = db.query(db_models.WorkoutHistory).filter(
        db_models.WorkoutHistory.id == workout_id,
        db_models.WorkoutHistory.user_id == current_user.id
    ).first()
    if not entry:
        raise HTTPException(status_code=404, detail="Workout not found")
    db.delete(entry)
    db.commit()
    return {"message": f"Workout {workout_id} deleted successfully"}
