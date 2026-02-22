from fastapi import APIRouter, Depends, HTTPException
from database.auth import get_current_user
from database import db as db_models
from models.schemas import (
    WorkoutPredictRequest, WorkoutPredictResponse,
    InjuryRiskRequest, InjuryRiskResponse,
    CalorieRequest, CalorieResponse
)
import sys, os
sys.path.insert(0, os.path.join(os.path.dirname(os.path.dirname(__file__)), "..", "fitness_ai_app_final"))

router = APIRouter(prefix="/ml", tags=["ML Predictions"])

@router.post("/workout-predict", response_model=WorkoutPredictResponse)
def predict_workout(data: WorkoutPredictRequest,
                    current_user: db_models.User = Depends(get_current_user)):
    try:
        from models.workout_model import predict_workout_level, get_model_stats, WORKOUT_PLANS
        level = predict_workout_level(
            age=data.age, bmi=data.bmi,
            experience_level=data.experience_level,
            goal=data.goal, activity_level=data.activity_level,
            weight=data.weight, height=data.height, gender=data.gender
        )
        stats = get_model_stats()
        plan  = WORKOUT_PLANS.get(level, {})
        return {
            "level":     level,
            "accuracy":  stats.get("accuracy", 0),
            "real_data": stats.get("real_data", False),
            "plan":      plan,
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/injury-risk", response_model=InjuryRiskResponse)
def predict_injury(data: InjuryRiskRequest,
                   current_user: db_models.User = Depends(get_current_user)):
    try:
        from models.injury_model import predict_injury_risk
        risk, color, confidence = predict_injury_risk(
            sleep=data.sleep, fatigue=data.fatigue,
            heart_rate=data.heart_rate, workout_freq=data.workout_freq
        )
        return {"risk": risk, "confidence": confidence, "color": color}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/calorie-predict", response_model=CalorieResponse)
def predict_calories(data: CalorieRequest,
                     current_user: db_models.User = Depends(get_current_user)):
    try:
        from models.calories_model import predict_calories, get_calories_model_stats
        cal   = predict_calories(
            age=data.age, weight=data.weight, height=data.height,
            duration_mins=data.duration, heart_rate=data.heart_rate,
            gender=data.gender
        )
        stats = get_calories_model_stats()
        return {"calories_burned": cal, "real_data": stats.get("real_data", False)}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/model-status")
def model_status(current_user: db_models.User = Depends(get_current_user)):
    """Returns status of all ML models."""
    try:
        from models.workout_model import get_model_stats
        from models.calories_model import get_calories_model_stats
        w_stats = get_model_stats()
        c_stats = get_calories_model_stats()
        return {
            "workout_model":  {"accuracy": w_stats.get("accuracy"), "real_data": w_stats.get("real_data"), "samples": w_stats.get("n_samples")},
            "calories_model": {"mae": c_stats.get("mae"), "r2": c_stats.get("r2"), "real_data": c_stats.get("real_data")},
            "injury_model":   {"type": "Logistic Regression", "classes": ["Low", "Medium", "High"]},
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
