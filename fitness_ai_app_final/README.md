# ⚡ FitAI Pro — Final Project
## BSc Data Science · University of Mumbai · 2025-2026

---

## 🚀 Quick Start

```bash
# 1. Install all libraries
py -m pip install streamlit scikit-learn pandas numpy plotly reportlab opencv-python mediapipe

# 2. Run the app
py -m streamlit run app.py
```

---

## 📁 Project Structure

```
fitness_ai_app_final/
├── app.py                      ← Main app (navigation + styling)
├── data/                       ← PUT YOUR CSV FILES HERE
│   ├── bodyPerformance.csv     ← Dataset 1
│   ├── calories.csv            ← Dataset 2
│   ├── exercise.csv            ← Dataset 2 (companion file)
│   └── food.csv                ← Dataset 3
├── models/
│   ├── workout_model.py        ← Random Forest (Body Performance)
│   ├── injury_model.py         ← Logistic Regression (synthetic)
│   ├── calories_model.py       ← Gradient Boosting (Calories)
│   └── nutrition_model.py      ← USDA food lookup
└── pages/
    ├── home.py                 ← Landing page
    ├── profile.py              ← BMI / BMR calculator
    ├── workout.py              ← AI workout recommendation
    ├── diet.py                 ← Diet plan
    ├── nutrition.py            ← Food nutrition analyser
    ├── calories.py             ← Calories burned predictor
    ├── injury.py               ← Injury risk prediction
    ├── score.py                ← Fitness score
    ├── dashboard.py            ← Analytics dashboard
    ├── chatbot.py              ← AI fitness chatbot
    ├── cv_exercise.py          ← Computer vision rep counter
    └── report.py               ← PDF export
```

---

## 📦 Dataset Download Instructions

### Dataset 1 — Body Performance (Workout Model)
- **URL:** https://www.kaggle.com/datasets/kukuroo3/body-performance-data
- **File to download:** `bodyPerformance.csv`
- **Save to:** `data/bodyPerformance.csv`
- **Records:** 13,393

### Dataset 2 — Calories Burned (Calories Predictor)
- **URL:** https://www.kaggle.com/datasets/fmendes/fmendesdat263xdemos
- **Files to download:** `calories.csv` AND `exercise.csv`
- **Save to:** `data/calories.csv` and `data/exercise.csv`
- **Records:** 15,000

### Dataset 3 — USDA Food Nutrition (Nutrition Analyser)
- **URL:** https://www.kaggle.com/datasets/thedevastator/usda-nutrition-database
- **File to download:** `food.csv` (or rename the main CSV to food.csv)
- **Save to:** `data/food.csv`
- **Records:** 8,000+

---

## 🤖 ML Models Summary

| Module | Algorithm | Dataset | Features | Output |
|---|---|---|---|---|
| Workout Recommendation | Random Forest (200 trees) | Body Performance | Age, Weight, Height, Gender, Situps, Broad Jump | Beginner/Intermediate/Advanced |
| Injury Risk | Logistic Regression | Synthetic (600 records) | Sleep, Fatigue, Heart Rate, Workout Freq | Low/Medium/High |
| Calories Burned | Gradient Boosting Regressor | Calories Burned | Age, Weight, Height, Duration, HR, Temp | kcal burned |
| Food Nutrition | Database Lookup | USDA Nutrition | Food name search | Macros per item |

---

## 🎓 Viva Preparation

**Q: What datasets did you use?**
> "The project uses three real-world datasets: the Kaggle Body Performance Dataset (13,393 records) for workout level prediction, the Calories Burned Dataset (15,000 records) for exercise calorie estimation using Gradient Boosting Regression, and the USDA Nutrition Database (8,000+ items) for food macro analysis."

**Q: Why Random Forest for workout recommendation?**
> "Random Forest handles non-linear relationships well, is resistant to overfitting, and provides feature importance scores. With 200 estimators trained on real body performance data, it achieved high classification accuracy across three fitness levels."

**Q: Why Gradient Boosting for calorie prediction?**
> "Calorie prediction is a regression task. Gradient Boosting builds sequential trees that correct previous errors, making it highly accurate for continuous value prediction. The model uses duration, heart rate, and body temperature as primary predictors."

**Q: How does the Computer Vision module work?**
> "The CV module uses MediaPipe Pose Estimation to detect 33 body landmarks in real time. Joint angles are calculated mathematically using the arctangent formula between three keypoints. When the knee angle crosses 90° during a squat, the system counts a rep and provides form feedback."

**Q: What is BMR and how is it calculated?**
> "BMR is Basal Metabolic Rate — calories burned at complete rest. It's calculated using the Mifflin-St Jeor equation. TDEE (Total Daily Energy Expenditure) is then calculated by multiplying BMR by an activity multiplier ranging from 1.2 (sedentary) to 1.9 (athlete)."

---

## ⚙️ Smart Dataset Fallback System

The app automatically detects whether real CSV files are present:
- ✅ CSV found → trains on real data, shows accuracy metrics
- ⚙️ CSV missing → uses synthetic data, shows yellow warning
- No code changes needed — just drop the CSV into `data/` and restart

---

*FitAI Pro · BSc Data Science · Sree Narayana Guru College of Commerce · Mumbai · 2025-2026*
