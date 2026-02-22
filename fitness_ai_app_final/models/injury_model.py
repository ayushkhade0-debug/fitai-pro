import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
import pickle
import os

def generate_injury_data():
    np.random.seed(42)
    n = 600
    sleep = np.random.uniform(3, 10, n)
    fatigue = np.random.randint(1, 11, n)
    heart_rate = np.random.randint(55, 120, n)
    workout_freq = np.random.randint(0, 8, n)
    risk_score = (10 - sleep) * 0.4 + fatigue * 0.4 + (heart_rate - 60) * 0.02 + workout_freq * 0.1
    labels = np.where(risk_score < 4, 0, np.where(risk_score < 7, 1, 2))
    return pd.DataFrame({
        "sleep": sleep, "fatigue": fatigue,
        "heart_rate": heart_rate, "workout_freq": workout_freq, "risk": labels
    })

def train_injury_model():
    model_path = os.path.join(os.path.dirname(__file__), "injury_model.pkl")
    if os.path.exists(model_path):
        with open(model_path, "rb") as f:
            return pickle.load(f)
    df = generate_injury_data()
    X = df[["sleep", "fatigue", "heart_rate", "workout_freq"]]
    y = df["risk"]
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)
    model = LogisticRegression(max_iter=500)
    model.fit(X_scaled, y)
    result = {"model": model, "scaler": scaler}
    with open(model_path, "wb") as f:
        pickle.dump(result, f)
    return result

def predict_injury_risk(sleep, fatigue, heart_rate, workout_freq=4):
    result = train_injury_model()
    model = result["model"]
    scaler = result["scaler"]
    X = scaler.transform([[sleep, fatigue, heart_rate, workout_freq]])
    pred = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    labels = {0: "Low", 1: "Medium", 2: "High"}
    colors = {0: "#00ffe7", 1: "#ffca28", 2: "#ff5252"}
    return labels[pred], colors[pred], round(max(proba) * 100, 1)
