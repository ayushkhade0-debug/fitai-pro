import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.calories_model import predict_calories, get_calories_model_stats
import plotly.graph_objects as go

EXERCISE_METS = {
    "Walking (slow)": 2.5, "Walking (brisk)": 3.5, "Jogging": 7.0,
    "Running": 9.8, "Cycling (light)": 5.0, "Cycling (intense)": 10.0,
    "Swimming": 6.0, "HIIT": 8.0, "Weight Training": 4.5,
    "Yoga": 2.5, "Football": 7.0, "Basketball": 6.5,
}

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 10 · Gradient Boosting</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            CALORIES BURNED PREDICTOR
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Gradient Boosting Regressor trained on real exercise &amp; calorie data
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.user_data:
        st.warning("⚠️ Complete Profile Setup first.")
        return

    u = st.session_state.user_data

    with st.form("calories_form"):
        col1, col2 = st.columns(2)
        with col1:
            exercise   = st.selectbox("🏃 Exercise Type", list(EXERCISE_METS.keys()))
            duration   = st.slider("⏱️ Duration (minutes)", 5, 120, 30)
        with col2:
            heart_rate = st.slider("❤️ Avg Heart Rate (bpm)", 60, 200, 130)
            intensity  = st.select_slider("💪 Intensity",
                             options=["Low", "Moderate", "High", "Maximum"],
                             value="Moderate")
        submitted = st.form_submit_button("⚡  PREDICT CALORIES BURNED")

    if submitted:
        adj_hr = heart_rate + {"Low": -15, "Moderate": 0, "High": 15, "Maximum": 30}[intensity]
        with st.spinner("Running Gradient Boosting model..."):
            ml_cal = predict_calories(
                age=u["age"], weight=u["weight"], height=u["height"],
                duration_mins=duration, heart_rate=adj_hr, gender=u["gender"]
            )
            stats = get_calories_model_stats()

        met = EXERCISE_METS.get(exercise, 5.0)
        met_cal = round(met * u["weight"] * (duration / 60), 1)
        st.session_state.user_data["last_calories_burned"] = ml_cal

        c1, c2, c3 = st.columns(3)
        c1.metric("🤖 ML Prediction", f"{ml_cal} kcal")
        c2.metric("📐 MET Formula",   f"{met_cal} kcal")
        c3.metric("⏱️ Duration",      f"{duration} min")

        fig = go.Figure(go.Indicator(
            mode="gauge+number", value=ml_cal,
            number={"font": {"family": "Orbitron", "color": "#ff6b35", "size": 36},
                    "suffix": " kcal"},
            gauge={
                "axis": {"range": [0, 800], "tickcolor": "#5a7a99",
                         "tickfont": {"color": "#5a7a99", "size": 10}},
                "bar": {"color": "#ff6b35", "thickness": 0.25},
                "bgcolor": "#0d1526", "bordercolor": "#1a2a45",
                "steps": [
                    {"range": [0, 200], "color": "#0a1520"},
                    {"range": [200, 500], "color": "#0d1a28"},
                    {"range": [500, 800], "color": "#1a1020"},
                ],
            }
        ))
        fig.update_layout(
            title=dict(text="Calories Burned", font=dict(family="Orbitron", color="white", size=13)),
            paper_bgcolor="#0d1526", font={"color": "white"},
            height=250, margin={"t": 40, "b": 10, "l": 20, "r": 20}
        )
        st.plotly_chart(fig, use_container_width=True)

        if stats["real_data"]:
            st.markdown(f"""
            <div style="background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.2);
                        border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem;">
                <span style="color:#00ffe7; font-size:0.8rem;">
                    ✅ Trained on <b>Kaggle Calories Dataset</b> —
                    {stats['n_samples']:,} records · R²: <b>{stats['r2']}%</b> · MAE: <b>{stats['mae']} kcal</b>
                </span>
            </div>""", unsafe_allow_html=True)
        else:
            st.markdown("""
            <div style="background:rgba(255,202,40,0.05); border:1px solid rgba(255,202,40,0.2);
                        border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1rem;">
                <span style="color:#ffca28; font-size:0.8rem;">
                    ⚙️ Place <b>calories.csv</b> + <b>exercise.csv</b> in <b>data/</b> folder for real predictions.
                </span>
            </div>""", unsafe_allow_html=True)

        tdee = u.get("tdee", 2000)
        pct  = round((ml_cal / tdee) * 100, 1)
        st.markdown(f"""
        <div class="ai-card">
            <div style="font-family:'Orbitron',monospace; color:#ff6b35; font-size:0.8rem; margin-bottom:0.8rem;">
                📊 SESSION ANALYSIS
            </div>
            <div style="color:#c8d8f0; font-size:0.85rem; line-height:2;">
                • Burned <b style="color:#ff6b35;">{ml_cal} kcal</b> —
                  <b style="color:#ff6b35;">{pct}%</b> of your daily TDEE ({tdee} kcal)<br>
                • Exercise: <b style="color:#00ffe7;">{exercise}</b> · {duration} min · {intensity} intensity<br>
                • Avg heart rate: <b style="color:#ff5252;">{heart_rate} bpm</b>
            </div>
        </div>""", unsafe_allow_html=True)
