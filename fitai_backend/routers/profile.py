from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.db import get_db
from database import db as db_models
from database.auth import get_current_user
from models.schemas import ProfileCreate, ProfileResponse
from datetime import datetime
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))

router = APIRouter(prefix="/profile", tags=["Profile"])

def calculate_bmi(weight, height):
    h = height / 100
    return round(weight / (h ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight"
    elif bmi < 25: return "Normal Weight"
    elif bmi < 30: return "Overweight"
    else:          return "Obese"

def calculate_bmr(weight, height, age, gender):
    if gender.lower() == "male":
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    return round(10 * weight + 6.25 * height - 5 * age - 161)

ACTIVITY_MULTIPLIERS = {
    "Sedentary (desk job, no exercise)":  1.2,
    "Lightly Active (1-3 days/week)":     1.375,
    "Moderately Active (3-5 days/week)":  1.55,
    "Very Active (6-7 days/week)":        1.725,
    "Athlete (2x/day training)":          1.9,
}

@router.post("/save", response_model=ProfileResponse)
def save_profile(data: ProfileCreate,
                 current_user: db_models.User = Depends(get_current_user),
                 db: Session = Depends(get_db)):
    bmi      = calculate_bmi(data.weight, data.height)
    bmi_cat  = bmi_category(bmi)
    bmr      = calculate_bmr(data.weight, data.height, data.age, data.gender)
    mult     = ACTIVITY_MULTIPLIERS.get(data.activity_level, 1.55)
    tdee     = round(bmr * mult)

    profile = db.query(db_models.UserProfile).filter(
        db_models.UserProfile.user_id == current_user.id).first()

    if profile:
        # Update existing
        profile.age            = data.age
        profile.gender         = data.gender
        profile.weight         = data.weight
        profile.height         = data.height
        profile.goal           = data.goal
        profile.activity_level = data.activity_level
        profile.experience     = data.experience
        profile.bmi            = bmi
        profile.bmi_category   = bmi_cat
        profile.bmr            = bmr
        profile.tdee           = tdee
        profile.updated_at     = datetime.utcnow()
    else:
        # Create new
        profile = db_models.UserProfile(
            user_id=current_user.id,
            age=data.age, gender=data.gender,
            weight=data.weight, height=data.height,
            goal=data.goal, activity_level=data.activity_level,
            experience=data.experience,
            bmi=bmi, bmi_category=bmi_cat,
            bmr=bmr, tdee=tdee,
        )
        db.add(profile)

    db.commit()
    db.refresh(profile)
    return profile

@router.get("/me", response_model=ProfileResponse)
def get_profile(current_user: db_models.User = Depends(get_current_user),
                db: Session = Depends(get_db)):
    profile = db.query(db_models.UserProfile).filter(
        db_models.UserProfile.user_id == current_user.id).first()
    if not profile:
        raise HTTPException(status_code=404, detail="Profile not found. Please create one first.")
    return profile
