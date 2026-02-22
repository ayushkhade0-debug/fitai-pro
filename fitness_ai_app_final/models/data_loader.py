"""
data_loader.py — Central data loading utility for FitAI Pro
Handles all 3 real datasets with automatic fallback to synthetic data
"""
import os
import pandas as pd
import numpy as np

BASE_DIR = os.path.dirname(os.path.dirname(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

BODY_PERF_PATH = os.path.join(DATA_DIR, "bodyPerformance.csv")
NUTRITION_PATH = os.path.join(DATA_DIR, "nutrition.csv")
EXERCISE_PATH  = os.path.join(DATA_DIR, "exercise.csv")
CALORIES_PATH  = os.path.join(DATA_DIR, "calories.csv")


# ── 1. Body Performance Dataset ───────────────────────────────────────────────
def load_body_performance():
    """Load Kaggle Body Performance dataset."""
    if not os.path.exists(BODY_PERF_PATH):
        return None, False

    try:
        df = pd.read_csv(BODY_PERF_PATH)
        df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")

        # Rename common variations
        rename_map = {}
        for col in df.columns:
            if "sit" in col and "up" in col:  rename_map[col] = "situps"
            if "broad" in col:                rename_map[col] = "broad_jump"
            if "height" in col:               rename_map[col] = "height_cm"
            if "weight" in col:               rename_map[col] = "weight_kg"
        df = df.rename(columns=rename_map)

        df["gender_enc"] = (df["gender"].str.strip().str.lower() == "m").astype(int)

        grade_map = {"A": "Advanced", "B": "Intermediate", "C": "Intermediate", "D": "Beginner"}
        df["workout_level"] = df["class"].map(grade_map)
        df = df.dropna(subset=["workout_level", "situps", "broad_jump", "height_cm", "weight_kg"])
        return df, True
    except Exception as e:
        print(f"[FitAI] Body Performance load error: {e}")
        return None, False


# ── 2. Nutrition Dataset ───────────────────────────────────────────────────────
def load_nutrition():
    """Load Nutrition dataset."""
    if not os.path.exists(NUTRITION_PATH):
        return None, False

    try:
        df = pd.read_csv(NUTRITION_PATH, encoding="utf-8", encoding_errors="replace")
        df.columns = df.columns.str.strip().str.lower()

        # Rename columns to standard names
        col_map = {}
        for col in df.columns:
            if col in ["name", "food", "item", "description"]:
                col_map[col] = "food_name"
            elif "calor" in col and col != "food_name":
                col_map[col] = "calories"
            elif col.startswith("protein"):
                col_map[col] = "protein"
            elif col.startswith("fat") or col == "total_fat" or col == "total fat":
                col_map[col] = "fat"
            elif "carb" in col:
                col_map[col] = "carbs"
            elif "fiber" in col:
                col_map[col] = "fiber"
            elif "sugar" in col:
                col_map[col] = "sugar"
            elif "sodium" in col:
                col_map[col] = "sodium"
        df = df.rename(columns=col_map)

        # If still no food_name, use index
        if "food_name" not in df.columns:
            df["food_name"] = df.index.astype(str)

        required = ["food_name", "calories", "protein", "fat", "carbs"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            print(f"[FitAI] Nutrition dataset missing columns: {missing}")
            return None, False

        df = df.dropna(subset=required)
        for col in ["calories", "protein", "fat", "carbs"]:
            df[col] = pd.to_numeric(df[col], errors="coerce")
        df = df.dropna(subset=required)
        df = df[df["calories"] > 0]
        df = df[df["calories"] < 2000]

        extra = [c for c in ["fiber", "sugar", "sodium"] if c in df.columns]
        return df[["food_name", "calories", "protein", "fat", "carbs"] + extra].reset_index(drop=True), True

    except PermissionError:
        print(f"[FitAI] nutrition.csv is open in another program. Close it and restart.")
        return None, False
    except Exception as e:
        print(f"[FitAI] Nutrition load error: {e}")
        return None, False


# ── 3. Exercise / Calories Burned Dataset ─────────────────────────────────────
def exercise_load():
    """Load Kaggle Exercise & Calories dataset — accepts exercise.csv OR calories.csv."""
    # Accept either filename
    path = None
    if os.path.exists(EXERCISE_PATH):
        path = EXERCISE_PATH
    elif os.path.exists(CALORIES_PATH):
        path = CALORIES_PATH

    if path is None:
        return None, False

    try:
        df = pd.read_csv(path, encoding="utf-8", encoding_errors="replace")
        df.columns = df.columns.str.strip().str.lower()

        col_map = {}
        for col in df.columns:
            if "calor" in col:    col_map[col] = "calories"
            if "duration" in col: col_map[col] = "duration"
            if "age" in col:      col_map[col] = "age"
            if "weight" in col:   col_map[col] = "weight"
            if "gender" in col:   col_map[col] = "gender"
            if "heart" in col:    col_map[col] = "heart_rate"
        df = df.rename(columns=col_map)

        required = ["calories"]
        missing = [c for c in required if c not in df.columns]
        if missing:
            return None, False

        df["calories"] = pd.to_numeric(df["calories"], errors="coerce")
        df = df.dropna(subset=["calories"])
        df = df[df["calories"] > 0]
        return df, True
    except PermissionError:
        print(f"[FitAI] calories.csv is open in another program. Close it and restart.")
        return None, False
    except Exception as e:
        print(f"[FitAI] Exercise load error: {e}")
        return None, False


# ── Dataset status summary ─────────────────────────────────────────────────────
def get_dataset_status():
    _, bp = load_body_performance()
    _, nu = load_nutrition()
    _, ex = exercise_load()
    return {
        "body_performance": bp,
        "nutrition":        nu,
        "exercise":         ex,
        "all_loaded":       bp and nu and ex,
        "count":            sum([bp, nu, ex]),
    }


# ── Synthetic fallbacks ────────────────────────────────────────────────────────
def synthetic_nutrition_foods():
    """Fallback food data when CSV not available."""
    return pd.DataFrame([
        {"food_name": "Chicken Breast (100g)", "calories": 165, "protein": 31, "fat": 3.6, "carbs": 0},
        {"food_name": "Brown Rice (100g)",      "calories": 216, "protein": 5,  "fat": 1.8, "carbs": 45},
        {"food_name": "Egg (1 large)",           "calories": 68,  "protein": 6,  "fat": 4.8, "carbs": 0.6},
        {"food_name": "Greek Yoghurt (100g)",    "calories": 59,  "protein": 10, "fat": 0.4, "carbs": 3.6},
        {"food_name": "Oats (100g)",             "calories": 389, "protein": 17, "fat": 7,   "carbs": 66},
        {"food_name": "Salmon (100g)",           "calories": 208, "protein": 20, "fat": 13,  "carbs": 0},
        {"food_name": "Banana (medium)",         "calories": 89,  "protein": 1,  "fat": 0.3, "carbs": 23},
        {"food_name": "Paneer (100g)",           "calories": 265, "protein": 18, "fat": 20,  "carbs": 3},
        {"food_name": "Sweet Potato (100g)",     "calories": 86,  "protein": 1.6,"fat": 0.1, "carbs": 20},
        {"food_name": "Almonds (30g)",           "calories": 173, "protein": 6,  "fat": 15,  "carbs": 6},
        {"food_name": "Lentils/Dal (100g)",      "calories": 116, "protein": 9,  "fat": 0.4, "carbs": 20},
        {"food_name": "Whey Protein (30g)",      "calories": 120, "protein": 24, "fat": 2,   "carbs": 3},
    ])
