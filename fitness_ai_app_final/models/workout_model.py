import numpy as np
import pickle, os
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder, StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

BASE_DIR   = os.path.dirname(__file__)
MODEL_PATH = os.path.join(BASE_DIR, "workout_model.pkl")

def train_model():
    from models.data_loader import load_body_performance, synthetic_nutrition_foods
    import sys
    sys.path.insert(0, os.path.dirname(BASE_DIR))

    csv_exists = os.path.exists(os.path.join(os.path.dirname(BASE_DIR), "data", "bodyPerformance.csv"))

    if os.path.exists(MODEL_PATH):
        with open(MODEL_PATH, "rb") as f:
            cached = pickle.load(f)
        if csv_exists and not cached.get("real_data", False):
            os.remove(MODEL_PATH)
        else:
            return cached

    using_real = False
    if csv_exists:
        try:
            df, ok = load_body_performance()
            if ok and df is not None:
                X = df[["age", "height_cm", "weight_kg", "gender_enc", "situps", "broad_jump"]].values
                y = df["workout_level"].values
                using_real = True
        except Exception:
            pass

    if not using_real:
        np.random.seed(42)
        n = 500
        age       = np.random.randint(18, 65, n)
        height    = np.random.uniform(150, 195, n)
        weight    = np.random.uniform(45, 110, n)
        gender    = np.random.choice([0, 1], n)
        situps    = np.random.randint(5, 80, n)
        broad     = np.random.randint(100, 280, n)
        X = np.column_stack([age, height, weight, gender, situps, broad])
        scores = situps * 0.4 + broad * 0.1
        y = np.where(scores < 18, "Beginner", np.where(scores >= 32, "Advanced", "Intermediate"))

    le     = LabelEncoder()
    y_enc  = le.fit_transform(y)
    scaler = StandardScaler()
    X_sc   = scaler.fit_transform(X)

    X_train, X_test, y_train, y_test = train_test_split(
        X_sc, y_enc, test_size=0.2, random_state=42, stratify=y_enc)

    model = RandomForestClassifier(n_estimators=200, max_depth=10,
                                   min_samples_split=4, random_state=42, n_jobs=-1)
    model.fit(X_train, y_train)

    acc    = round(accuracy_score(y_test, model.predict(X_test)) * 100, 1)
    report = classification_report(y_test, model.predict(X_test),
                                   target_names=le.classes_, output_dict=True)

    result = {"model": model, "encoder": le, "scaler": scaler,
              "accuracy": acc, "report": report,
              "real_data": using_real, "n_samples": len(X)}
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(result, f)
    return result

def get_model_stats():
    r = train_model()
    return {"accuracy": r.get("accuracy","N/A"),
            "real_data": r.get("real_data", False),
            "n_samples": r.get("n_samples", 0)}

def predict_workout_level(age, bmi, experience_level, goal, activity_level,
                          weight=70, height=170, gender="Male"):
    r = train_model()
    model, le, scaler = r["model"], r["encoder"], r["scaler"]
    exp_situps = {"Beginner": 20, "Intermediate": 45, "Advanced": 70}
    exp_jump   = {"Beginner": 150, "Intermediate": 200, "Advanced": 250}
    g_enc = 1 if gender == "Male" else 0
    X = scaler.transform([[age, height, weight, g_enc,
                           exp_situps.get(experience_level, 30),
                           exp_jump.get(experience_level, 180)]])
    return le.inverse_transform(r["model"].predict(X))[0]

WORKOUT_PLANS = {
    "Beginner": {
        "description": "3 days/week full body training. Focus on form and building habits.",
        "days": {
            "Monday":    ["Bodyweight Squats 3×15", "Push-ups 3×10", "Plank 3×30s", "Walking 20 min"],
            "Wednesday": ["Dumbbell Rows 3×12", "Glute Bridges 3×15", "Wall Sit 3×30s", "Cycling 20 min"],
            "Friday":    ["Lunges 3×12", "Shoulder Press 3×10", "Sit-ups 3×15", "Stretching 15 min"],
        }
    },
    "Intermediate": {
        "description": "4-5 days/week split training. Progressive overload focus.",
        "days": {
            "Monday":   ["Barbell Squat 4×10", "Bench Press 4×10", "Pull-ups 3×8", "Cable Rows 3×12"],
            "Tuesday":  ["Deadlift 4×6", "Romanian DL 3×10", "Leg Press 3×12", "Calf Raises 4×15"],
            "Thursday": ["Overhead Press 4×8", "Dips 3×10", "Tricep Pushdowns 3×12", "Lateral Raises 3×15"],
            "Friday":   ["Incline Press 4×10", "Barbell Curls 3×12", "Face Pulls 3×15", "Cardio 30 min"],
        }
    },
    "Advanced": {
        "description": "5-6 days/week PPL split. Periodisation & intensity techniques.",
        "days": {
            "Monday (Push)":    ["Bench Press 5×5", "Incline DB Press 4×10", "OHP 4×8", "Lateral Raises 4×15"],
            "Tuesday (Pull)":   ["Deadlift 5×3", "Weighted Pull-ups 4×8", "Barbell Rows 4×10", "Face Pulls 4×15"],
            "Wednesday (Legs)": ["Back Squat 5×5", "RDL 4×10", "Hack Squat 4×12", "Leg Curl 3×15"],
            "Friday (Push)":    ["Incline Press 5×6", "Cable Fly 4×12", "Arnold Press 4×10"],
            "Saturday (Pull)":  ["Power Cleans 5×3", "T-Bar Rows 4×10", "Lat Pulldown 4×12"],
        }
    }
}
