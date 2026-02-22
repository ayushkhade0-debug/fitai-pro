from pydantic import BaseModel
from typing import Optional
from datetime import datetime

# ── Auth Schemas ───────────────────────────────────────────────────────────────
class RegisterRequest(BaseModel):
    name:     str
    email:    str
    password: str

class LoginRequest(BaseModel):
    email:    str
    password: str

class TokenResponse(BaseModel):
    access_token: str
    token_type:   str = "bearer"
    user_id:      int
    name:         str

# ── Profile Schemas ────────────────────────────────────────────────────────────
class ProfileCreate(BaseModel):
    age:            int
    gender:         str
    weight:         float
    height:         float
    goal:           str
    activity_level: str
    experience:     str

class ProfileResponse(BaseModel):
    age:            int
    gender:         str
    weight:         float
    height:         float
    goal:           str
    activity_level: str
    experience:     str
    bmi:            Optional[float]
    bmi_category:   Optional[str]
    bmr:            Optional[float]
    tdee:           Optional[float]
    workout_level:  Optional[str]
    injury_risk:    Optional[str]
    fitness_score:  Optional[float]
    updated_at:     Optional[datetime]

    class Config:
        from_attributes = True

# ── ML Prediction Schemas ──────────────────────────────────────────────────────
class WorkoutPredictRequest(BaseModel):
    age:              int
    bmi:              float
    experience_level: str
    goal:             str
    activity_level:   str
    weight:           float
    height:           float
    gender:           str

class WorkoutPredictResponse(BaseModel):
    level:     str
    accuracy:  float
    real_data: bool
    plan:      dict

class InjuryRiskRequest(BaseModel):
    sleep:        float
    fatigue:      int
    heart_rate:   int
    workout_freq: int

class InjuryRiskResponse(BaseModel):
    risk:       str
    confidence: float
    color:      str

class CalorieRequest(BaseModel):
    age:          int
    weight:       float
    height:       float
    duration:     int
    heart_rate:   int
    gender:       str

class CalorieResponse(BaseModel):
    calories_burned: float
    real_data:       bool

# ── Workout History Schemas ────────────────────────────────────────────────────
class WorkoutLogRequest(BaseModel):
    exercise: str
    duration: int
    calories: float
    sets:     int
    reps:     int
    notes:    Optional[str] = ""

class WorkoutLogResponse(BaseModel):
    id:        int
    exercise:  str
    duration:  int
    calories:  float
    sets:      int
    reps:      int
    notes:     Optional[str]
    logged_at: datetime

    class Config:
        from_attributes = True

# ── General ────────────────────────────────────────────────────────────────────
class MessageResponse(BaseModel):
    message: str
