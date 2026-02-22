from sqlalchemy import create_engine, Column, Integer, String, Float, DateTime, ForeignKey, Text
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, relationship
from datetime import datetime
import os

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATABASE_URL = f"sqlite:///{os.path.join(BASE_DIR, 'fitai.db')}"

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# ── Database Models ────────────────────────────────────────────────────────────

class User(Base):
    __tablename__ = "users"
    id            = Column(Integer, primary_key=True, index=True)
    name          = Column(String, nullable=False)
    email         = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)
    created_at    = Column(DateTime, default=datetime.utcnow)

    profile       = relationship("UserProfile", back_populates="user", uselist=False)
    workouts      = relationship("WorkoutHistory", back_populates="user")

class UserProfile(Base):
    __tablename__ = "user_profiles"
    id             = Column(Integer, primary_key=True, index=True)
    user_id        = Column(Integer, ForeignKey("users.id"), unique=True)
    age            = Column(Integer)
    gender         = Column(String)
    weight         = Column(Float)
    height         = Column(Float)
    goal           = Column(String)
    activity_level = Column(String)
    experience     = Column(String)
    bmi            = Column(Float)
    bmi_category   = Column(String)
    bmr            = Column(Float)
    tdee           = Column(Float)
    workout_level  = Column(String)
    injury_risk    = Column(String)
    fitness_score  = Column(Float)
    updated_at     = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    user = relationship("User", back_populates="profile")

class WorkoutHistory(Base):
    __tablename__ = "workout_history"
    id           = Column(Integer, primary_key=True, index=True)
    user_id      = Column(Integer, ForeignKey("users.id"))
    exercise     = Column(String)
    duration     = Column(Integer)
    calories     = Column(Float)
    sets         = Column(Integer)
    reps         = Column(Integer)
    notes        = Column(Text, nullable=True)
    logged_at    = Column(DateTime, default=datetime.utcnow)

    user = relationship("User", back_populates="workouts")

def create_tables():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
