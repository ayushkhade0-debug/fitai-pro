# FitAI Pro — FastAPI Backend

## Setup Instructions

### Step 1 — Install dependencies
```
cd fitai_backend
py -m pip install -r requirements.txt
```

### Step 2 — Start the backend
```
uvicorn main:app --reload
```

Backend runs at: http://127.0.0.1:8000

### Step 3 — View API docs
Open browser: http://127.0.0.1:8000/docs

### Step 4 — Start the frontend (in a NEW terminal)
```
cd fitness_ai_app_final
py -m streamlit run app.py
```

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| POST | /auth/register | Create new account |
| POST | /auth/login | Login, get JWT token |
| POST | /profile/save | Save user profile |
| GET  | /profile/me | Get current profile |
| POST | /ml/workout-predict | Predict workout level |
| POST | /ml/injury-risk | Predict injury risk |
| POST | /ml/calorie-predict | Predict calories burned |
| GET  | /ml/model-status | ML model stats |
| POST | /workouts/log | Log a workout session |
| GET  | /workouts/history | Get workout history |
| GET  | /workouts/stats | Get workout summary |
| DELETE | /workouts/delete/{id} | Delete a workout |

---

## Tech Stack
- **FastAPI** — REST API framework
- **SQLite** — Database (auto-created as fitai.db)
- **SQLAlchemy** — ORM
- **JWT** — Authentication tokens
- **passlib** — Password hashing (bcrypt)
