import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.injury_model import predict_injury_risk

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 04 · Logistic Regression</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            INJURY RISK ANALYSIS
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Multinomial classifier trained on 600 synthetic samples · 4-feature input vector
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("injury_form"):
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
            Input Parameters
        </div>
        """, unsafe_allow_html=True)

        col1, col2 = st.columns(2)
        with col1:
            sleep = st.slider("😴  Sleep Duration (hours)", 2.0, 12.0, 7.0, 0.5)
            heart_rate = st.number_input("❤️  Resting Heart Rate (bpm)", 40, 200, 72)
        with col2:
            fatigue = st.slider("😓  Fatigue Level  (1 = Fresh · 10 = Exhausted)", 1, 10, 3)
            workout_freq = st.slider("🏋️  Training Sessions This Week", 0, 14, 4)

        submitted = st.form_submit_button("⚡  RUN RISK ASSESSMENT")

    if submitted:
        with st.spinner("Running Logistic Regression model..."):
            risk, color, confidence = predict_injury_risk(sleep, fatigue, heart_rate, workout_freq)

        st.session_state.user_data["injury_risk"] = risk

        icons = {"Low": "🟢", "Medium": "🟡", "High": "🔴"}
        st.markdown(f"""
        <div class="ai-card" style="border-color:{color}44; text-align:center; padding:2.5rem;">
            <div style="font-size:3rem; margin-bottom:0.5rem;">{icons.get(risk,'⚡')}</div>
            <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.5rem;">
                Injury Risk Classification
            </div>
            <div style="font-family:'Orbitron',monospace; font-size:2.5rem; color:{color}; font-weight:900; letter-spacing:4px;">
                {risk.upper()} RISK
            </div>
            <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.8rem;">
                Model confidence: <span style="color:{color}; font-family:'Orbitron',monospace;">{confidence}%</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        # Input summary
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Sleep", f"{sleep}h")
        c2.metric("Heart Rate", f"{heart_rate} bpm")
        c3.metric("Fatigue", f"{fatigue}/10")
        c4.metric("Sessions/Week", workout_freq)

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.8rem;">
            Recommendations
        </div>
        """, unsafe_allow_html=True)

        if risk == "Low":
            recs = [
                ("✅", "Cleared for full training intensity", "#00ffe7"),
                ("💧", "Maintain hydration — 2.5–3L water daily", "#00ffe7"),
                ("🔥", "Include a 10-minute dynamic warm-up before each session", "#00ffe7"),
                ("😴", "Continue current sleep schedule — excellent recovery", "#00ffe7"),
            ]
        elif risk == "Medium":
            recs = [
                ("⚠️", "Reduce training intensity by 20–30% today", "#ffca28"),
                ("🧘", "Add 15 minutes of foam rolling and stretching", "#ffca28"),
                ("😴", "Target 8 hours sleep tonight to aid recovery", "#ffca28"),
                ("🚫", "Avoid high-impact exercises if experiencing any discomfort", "#ffca28"),
            ]
        else:
            recs = [
                ("🛑", "REST DAY RECOMMENDED — Do not train today", "#ff5252"),
                ("🏥", "Consult a physiotherapist if pain persists beyond 48 hours", "#ff5252"),
                ("😴", "Prioritise 9 hours of sleep with no screen time before bed", "#ff5252"),
                ("💊", "Consider anti-inflammatory measures if joints are affected", "#ff5252"),
            ]

        for icon, text, color in recs:
            st.markdown(f"""
            <div style="display:flex; gap:1rem; align-items:center; padding:0.75rem 1rem;
                        background:#0d1526; border-radius:6px; border-left:3px solid {color};
                        margin-bottom:0.4rem;">
                <span style="font-size:1.1rem;">{icon}</span>
                <span style="color:#c8d8f0; font-size:0.85rem;">{text}</span>
            </div>
            """, unsafe_allow_html=True)
