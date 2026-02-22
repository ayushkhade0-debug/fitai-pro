import pandas as pd
import numpy as np
import pickle, os

BASE_DIR   = os.path.dirname(__file__)
DATA_PATH  = os.path.join(BASE_DIR, "..", "data", "food.csv")
CACHE_PATH = os.path.join(BASE_DIR, "nutrition_data.pkl")

def load_real_dataset():
    df = pd.read_csv(DATA_PATH)
    df.columns = df.columns.str.strip().str.lower().str.replace(" ", "_")
    name_col = next((c for c in df.columns if "name" in c or "descrip" in c), None)
    cal_col  = next((c for c in df.columns if "calor" in c or "energy" in c), None)
    prot_col = next((c for c in df.columns if "protein" in c), None)
    carb_col = next((c for c in df.columns if "carb" in c), None)
    fat_col  = next((c for c in df.columns if "fat" in c or "lipid" in c), None)
    if not all([name_col, cal_col, prot_col]):
        raise ValueError("Required columns not found")
    df = df[[name_col, cal_col, prot_col, carb_col, fat_col]].dropna()
    df.columns = ["name", "calories", "protein", "carbs", "fat"]
    return df[df["calories"] > 0].head(500)

def get_synthetic_nutrition():
    foods = [
        ("Chicken Breast (100g)", 165, 31, 0, 3.6),
        ("Brown Rice (100g)", 216, 5, 45, 1.8),
        ("Egg (1 whole)", 78, 6, 0.6, 5),
        ("Oats (100g)", 389, 17, 66, 7),
        ("Banana (medium)", 89, 1.1, 23, 0.3),
        ("Greek Yoghurt (100g)", 59, 10, 3.6, 0.4),
        ("Salmon (100g)", 208, 20, 0, 13),
        ("Paneer (100g)", 265, 18, 3.4, 20),
        ("Sweet Potato (100g)", 86, 1.6, 20, 0.1),
        ("Almonds (30g)", 174, 6, 6, 15),
        ("Avocado (half)", 120, 1.5, 6, 11),
        ("Quinoa (100g)", 222, 8, 39, 3.6),
        ("Lentils/Dal (100g)", 116, 9, 20, 0.4),
        ("Whey Protein (30g)", 120, 24, 3, 2),
        ("Apple (medium)", 95, 0.5, 25, 0.3),
        ("Cottage Cheese (100g)", 98, 11, 3.4, 4.3),
        ("Tuna (100g)", 144, 30, 0, 3.2),
        ("Broccoli (100g)", 34, 2.8, 7, 0.4),
        ("Whole Milk (200ml)", 122, 6.4, 9.6, 6.4),
        ("Peanut Butter (30g)", 188, 8, 6, 16),
    ]
    return pd.DataFrame(foods, columns=["name","calories","protein","carbs","fat"])

def get_nutrition_data():
    if os.path.exists(CACHE_PATH):
        with open(CACHE_PATH, "rb") as f:
            cached = pickle.load(f)
        if os.path.exists(DATA_PATH) and not cached.get("real_data", False):
            os.remove(CACHE_PATH)
        else:
            return cached
    using_real = False
    if os.path.exists(DATA_PATH):
        try:
            df = load_real_dataset()
            using_real = True
        except:
            df = get_synthetic_nutrition()
    else:
        df = get_synthetic_nutrition()
    result = {"data": df, "real_data": using_real, "n_samples": len(df)}
    with open(CACHE_PATH, "wb") as f:
        pickle.dump(result, f)
    return result

def search_foods(query="", top_n=10):
    result = get_nutrition_data()
    df = result["data"]
    if query:
        mask = df["name"].str.lower().str.contains(query.lower(), na=False)
        filtered = df[mask].head(top_n)
        if filtered.empty:
            filtered = df.head(top_n)
    else:
        filtered = df.head(top_n)
    return filtered, result["real_data"], result["n_samples"]
