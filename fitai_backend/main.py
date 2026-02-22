from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from database.db import create_tables
from routers import auth, profile, ml, workouts

# ── Create app ─────────────────────────────────────────────────────────────────
app = FastAPI(
    title="FitAI Pro — Backend API",
    description="""
## FitAI Pro REST API

Backend for the FitAI Pro Intelligent Fitness Management System.

### Features:
- **Authentication** — JWT-based login & registration
- **Profile** — Save and retrieve user biometrics
- **ML Models** — Workout prediction, injury risk, calorie estimation
- **Workout History** — Log and track workout sessions

### BSc Data Science Final Year Project
**Student:** Ayush Khade  
**Institution:** Sree Narayana Guru College of Commerce, Mumbai  
**Tech Stack:** FastAPI · SQLite · SQLAlchemy · scikit-learn · JWT
    """,
    version="1.0.0",
)

# ── CORS — allow Streamlit frontend to call the API ────────────────────────────
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ── Create database tables on startup ─────────────────────────────────────────
@app.on_event("startup")
def startup():
    create_tables()
    print("✅ FitAI Backend started — database ready")

# ── Include routers ────────────────────────────────────────────────────────────
app.include_router(auth.router)
app.include_router(profile.router)
app.include_router(ml.router)
app.include_router(workouts.router)

# ── Health check ───────────────────────────────────────────────────────────────
@app.get("/", tags=["Health"])
def root():
    return {
        "status":  "✅ FitAI Pro Backend is running",
        "version": "1.0.0",
        "docs":    "Visit /docs for interactive API documentation",
    }

@app.get("/health", tags=["Health"])
def health():
    return {"status": "healthy", "database": "SQLite connected"}
