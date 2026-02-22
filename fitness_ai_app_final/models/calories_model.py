import pandas as pd
import numpy as np
from sklearn.ensemble import GradientBoostingRegressor
from sklearn.preprocessing import StandardScaler
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, r2_score
import pickle, os

BASE_DIR   = os.path.dirname(__file__)
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "calories.csv")
EX_PATH    = os.path.join(BASE_DIR, "..", "data", "exercise.csv")
MODEL_PATH = os.path.join(BASE_DIR, "calories_model.pkl")

def load_real_dataset():
    # Accept calories.csv directly
    cal_path = DATA_PATH if os.path.exists(DATA_PATH) else EX_PATH
    df = pd.read_csv(cal_path, encoding="utf-8", encoding_errors="replace")
    df.columns = df.columns.str.strip().str.lower()
    col_map = {}
    for col in df.columns:
        if "calor" in col:    col_map[col] = "calories"
        if "duration" in col: col_map[col] = "duration"
        if "age" in col:      col_map[col] = "age"
        if "weight" in col:   col_map[col] = "weight"
        if "height" in col:   col_map[col] = "height"
        if "gender" in col:   col_map[col] = "gender"
        if "heart" in col:    col_map[col] = "heart_rate"
        if "temp" in col:     col_map[col] = "body_temp"
    df = df.rename(columns=col_map)
    df["gender_enc"] = (df.get("gender", pd.Series(["male"]*len(df))).str.lower() == "male").astype(int)
    # Use available features
    available = [c for c in ["age", "height", "weight", "duration", "heart_rate", "body_temp", "gender_enc"] if c in df.columns]
    df = df.dropna(subset=available + ["calories"])
    return df[available].values, df["calories"].values, available

def generate_synthetic_dataset():
    np.random.seed(99)
    n = 1000
    age = np.random.randint(18, 65, n)
    weight = np.random.uniform(50, 110, n)
    height = np.random.uniform(155, 195, n)
    duration = np.random.uniform(10, 60, n)
    hr = np.random.uniform(80, 170, n)
    temp = np.random.uniform(37, 41, n)
    gender = np.random.choice([0, 1], n)
    calories = (duration * 0.074 * weight + hr * 0.4 +
                temp * 2.0 - 20 + np.random.normal(0, 5, n))
    return np.column_stack([age, height, weight, duration, hr, temp, gender]), np.clip(calories, 30, 600)

def train_model():
    csv_exists = os.path.exists(DATA_PATH) or os.path.exists(EX_PATH)
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
            X, y, _ = load_real_dataset()
            using_real = True
        except Exception:
            X, y = generate_synthetic_dataset()
    else:
        X, y = generate_synthetic_dataset()

    scaler = StandardScaler()
    X_s = scaler.fit_transform(X)
    X_train, X_test, y_train, y_test = train_test_split(X_s, y, test_size=0.2, random_state=42)
    model = GradientBoostingRegressor(n_estimators=200, max_depth=5, learning_rate=0.05, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    result = {"model": model, "scaler": scaler,
              "mae": round(mean_absolute_error(y_test, y_pred), 2),
              "r2": round(r2_score(y_test, y_pred), 3),
              "real_data": using_real, "n_samples": len(X)}
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(result, f)
    return result

def predict_calories(age, weight, height, duration_mins, heart_rate=120, body_temp=38.5, gender="Male"):
    r = train_model()
    X = r["scaler"].transform([[age, height, weight, duration_mins,
                                heart_rate, body_temp, 1 if gender=="Male" else 0]])
    return round(float(r["model"].predict(X)[0]), 1)

def get_calories_model_stats():
    r = train_model()
    return {"mae": r.get("mae","N/A"), "r2": r.get("r2","N/A"),
            "real_data": r.get("real_data", False), "n_samples": r.get("n_samples", 0)}
