import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.data_loader import load_nutrition, synthetic_nutrition_foods

MEAL_PLANS = {
    "Weight Loss":       {"calorie_adjust": -500, "protein_ratio": 0.35, "carb_ratio": 0.40, "fat_ratio": 0.25},
    "Muscle Gain":       {"calorie_adjust":  300, "protein_ratio": 0.40, "carb_ratio": 0.40, "fat_ratio": 0.20},
    "Maintain Fitness":  {"calorie_adjust":    0, "protein_ratio": 0.30, "carb_ratio": 0.45, "fat_ratio": 0.25},
    "Improve Endurance": {"calorie_adjust":  200, "protein_ratio": 0.25, "carb_ratio": 0.55, "fat_ratio": 0.20},
    "General Health":    {"calorie_adjust":    0, "protein_ratio": 0.30, "carb_ratio": 0.45, "fat_ratio": 0.25},
}

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 03 · Nutrition Dataset</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            NUTRITION RECOMMENDATION ENGINE
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Real food nutrition data · BMR-based calorie targets · macro optimisation
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.user_data:
        st.warning("⚠️ Complete Profile Setup first.")
        return

    u = st.session_state.user_data
    goal   = u.get("goal", "General Health")
    tdee   = u.get("tdee", 2000)
    weight = u.get("weight", 70)

    plan       = MEAL_PLANS.get(goal, MEAL_PLANS["General Health"])
    target_cal = tdee + plan["calorie_adjust"]
    protein_g  = round(target_cal * plan["protein_ratio"] / 4)
    carbs_g    = round(target_cal * plan["carb_ratio"] / 4)
    fat_g      = round(target_cal * plan["fat_ratio"] / 9)
    water_l    = round(weight * 0.033, 1)

    st.session_state.user_data["diet_calories"] = target_cal
    st.session_state.user_data["diet_protein"]  = protein_g

    # Load nutrition dataset
    nutrition_df, real_data = load_nutrition()
    if nutrition_df is None:
        nutrition_df = synthetic_nutrition_foods()
        real_data = False

    # Goal banner
    adj = plan["calorie_adjust"]
    adj_text = f"+{adj}" if adj > 0 else (str(adj) if adj < 0 else "±0")
    st.markdown(f"""
    <div class="ai-card" style="display:flex; justify-content:space-between; align-items:center;">
        <div>
            <div class="stat-label">Active Goal</div>
            <div style="font-family:'Orbitron',monospace; font-size:1rem; color:#00ffe7; margin-top:0.3rem;">{goal.upper()}</div>
        </div>
        <div style="text-align:center;">
            <div class="stat-label">Data Source</div>
            <div style="font-size:0.8rem; margin-top:0.3rem; color:{'#00ffe7' if real_data else '#ffca28'};">
                {'✅ Real Nutrition Dataset' if real_data else '⚙️ Synthetic Data'}
            </div>
        </div>
        <div style="text-align:right;">
            <div class="stat-label">Calorie Adjustment</div>
            <div style="font-family:'Orbitron',monospace; font-size:1rem; color:{'#ff6b35' if adj<0 else '#00ffe7'}; margin-top:0.3rem;">{adj_text} kcal/day</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Macro metrics
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("🔥 Daily Calories", f"{target_cal} kcal")
    c2.metric("🥩 Protein", f"{protein_g}g")
    c3.metric("🍚 Carbohydrates", f"{carbs_g}g")
    c4.metric("🥑 Fats", f"{fat_g}g")

    st.markdown("<br>", unsafe_allow_html=True)

    # Macro bars
    st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
    text-transform:uppercase; margin-bottom:0.8rem;">Macro Distribution</div>""", unsafe_allow_html=True)

    for label, ratio, color, amount in [
        ("Protein",       plan["protein_ratio"], "#00ffe7", f"{protein_g}g"),
        ("Carbohydrates", plan["carb_ratio"],    "#00b8ff", f"{carbs_g}g"),
        ("Fats",          plan["fat_ratio"],      "#ff6b35", f"{fat_g}g"),
    ]:
        st.markdown(f"""
        <div style="margin-bottom:0.8rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                <span style="color:#c8d8f0; font-size:0.8rem;">{label}</span>
                <span style="color:{color}; font-family:'Orbitron',monospace; font-size:0.75rem;">
                    {int(ratio*100)}% · {amount}
                </span>
            </div>
            <div style="background:#111d35; border-radius:3px; height:5px;">
                <div style="width:{int(ratio*100)}%; height:100%; background:{color}; border-radius:3px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Real food search from dataset ────────────────────────────────────────
    st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
    text-transform:uppercase; margin-bottom:0.8rem;">🔍 Food Nutrition Search
    """ + (" <span style='color:#00ffe7; font-size:0.65rem;'>(Real Dataset)</span>" if real_data
           else " <span style='color:#ffca28; font-size:0.65rem;'>(Add nutrition.csv for full search)</span>") +
    "</div>", unsafe_allow_html=True)

    search = st.text_input("Search food item", placeholder="e.g. chicken, rice, egg, banana...")

    if search:
        mask = nutrition_df["food_name"].str.contains(search, case=False, na=False)
        results = nutrition_df[mask].head(10)
        if len(results) > 0:
            for _, row in results.iterrows():
                st.markdown(f"""
                <div style="display:flex; justify-content:space-between; align-items:center;
                            padding:0.7rem 1rem; background:#0d1526;
                            border-radius:8px; border-left:3px solid #00ffe7; margin-bottom:0.4rem;">
                    <span style="color:#c8d8f0; font-size:0.85rem; flex:2;">{row['food_name']}</span>
                    <span style="color:#00ffe7; font-family:'Orbitron',monospace; font-size:0.75rem; flex:1; text-align:center;">
                        {int(row['calories'])} kcal
                    </span>
                    <span style="color:#5a7a99; font-size:0.75rem; flex:2; text-align:right;">
                        P: {round(row['protein'],1)}g · C: {round(row['carbs'],1)}g · F: {round(row['fat'],1)}g
                    </span>
                </div>
                """, unsafe_allow_html=True)
        else:
            st.info("No foods found. Try a different search term.")

    st.markdown("<br>", unsafe_allow_html=True)

    # ── Top high-protein foods from dataset ──────────────────────────────────
    st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
    text-transform:uppercase; margin-bottom:0.8rem;">Top High-Protein Foods</div>""", unsafe_allow_html=True)

    top_protein = nutrition_df.nlargest(8, "protein")
    for _, row in top_protein.iterrows():
        pct = min(int(row["protein"] / 50 * 100), 100)
        st.markdown(f"""
        <div style="margin-bottom:0.6rem;">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.2rem;">
                <span style="color:#c8d8f0; font-size:0.8rem;">{row['food_name']}</span>
                <span style="color:#00ffe7; font-family:'Orbitron',monospace; font-size:0.72rem;">
                    {round(row['protein'],1)}g protein · {int(row['calories'])} kcal
                </span>
            </div>
            <div style="background:#111d35; border-radius:3px; height:4px;">
                <div style="width:{pct}%; height:100%; background:#00ffe7; border-radius:3px;"></div>
            </div>
        </div>
        """, unsafe_allow_html=True)

    st.markdown(f"""
    <div style="margin-top:1rem; background:rgba(0,184,255,0.05); border:1px solid rgba(0,184,255,0.2);
                border-radius:8px; padding:1rem; display:flex; gap:1rem; align-items:center;">
        <span style="font-size:1.5rem;">💧</span>
        <span style="color:#c8d8f0; font-size:0.85rem;">
            Daily hydration target: <b style="color:#00b8ff; font-family:'Orbitron',monospace;">{water_l}L</b>
            based on your body weight of {weight}kg
        </span>
    </div>
    """, unsafe_allow_html=True)
