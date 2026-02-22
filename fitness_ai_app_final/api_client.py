"""
api_client.py — Streamlit frontend API client
Handles all HTTP requests to the FastAPI backend
"""
import requests
import streamlit as st

BASE_URL = "https://fitai-backend-69an.onrender.com"
```

def get_headers():
    token = st.session_state.get("token", "")
    return {"Authorization": f"Bearer {token}"}

# ── Auth ───────────────────────────────────────────────────────────────────────
def register(name, email, password):
    try:
        r = requests.post(f"{BASE_URL}/auth/register",
                          json={"name": name, "email": email, "password": password})
        return r.json(), r.status_code == 200
    except Exception:
        return {"message": "❌ Backend not running. Start it first."}, False

def login(email, password):
    try:
        r = requests.post(f"{BASE_URL}/auth/login",
                          json={"email": email, "password": password})
        return r.json(), r.status_code == 200
    except Exception:
        return {"message": "❌ Backend not running. Start it first."}, False

# ── Profile ────────────────────────────────────────────────────────────────────
def save_profile(profile_data):
    try:
        r = requests.post(f"{BASE_URL}/profile/save",
                          json=profile_data, headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {"detail": "Backend error"}, False

def get_profile():
    try:
        r = requests.get(f"{BASE_URL}/profile/me", headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

# ── ML ─────────────────────────────────────────────────────────────────────────
def predict_workout(payload):
    try:
        r = requests.post(f"{BASE_URL}/ml/workout-predict",
                          json=payload, headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

def predict_injury(payload):
    try:
        r = requests.post(f"{BASE_URL}/ml/injury-risk",
                          json=payload, headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

def predict_calories_api(payload):
    try:
        r = requests.post(f"{BASE_URL}/ml/calorie-predict",
                          json=payload, headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

def get_model_status():
    try:
        r = requests.get(f"{BASE_URL}/ml/model-status", headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

# ── Workouts ───────────────────────────────────────────────────────────────────
def log_workout(payload):
    try:
        r = requests.post(f"{BASE_URL}/workouts/log",
                          json=payload, headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

def get_workout_history():
    try:
        r = requests.get(f"{BASE_URL}/workouts/history", headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return [], False

def get_workout_stats():
    try:
        r = requests.get(f"{BASE_URL}/workouts/stats", headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

def delete_workout(workout_id):
    try:
        r = requests.delete(f"{BASE_URL}/workouts/delete/{workout_id}",
                            headers=get_headers())
        return r.json(), r.status_code == 200
    except Exception:
        return {}, False

# ── Backend health check ───────────────────────────────────────────────────────
def check_backend():
    try:
        r = requests.get(f"{BASE_URL}/health", timeout=30)
        return r.status_code == 200
    except Exception:
        return False
