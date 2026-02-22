import streamlit as st
import sys, os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))
from models.workout_model import predict_workout_level, get_model_stats, WORKOUT_PLANS

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 02 · Random Forest ML</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            AI WORKOUT RECOMMENDATION
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            200-tree Random Forest classifier trained on real body performance data
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.user_data:
        st.warning("⚠️ Complete Profile Setup first.")
        return

    u = st.session_state.user_data

    with st.spinner("Running Random Forest inference..."):
        level = predict_workout_level(
            age=u["age"], bmi=u["bmi"],
            experience_level=u["fitness_experience"],
            goal=u["goal"], activity_level=u["activity_level"],
            weight=u.get("weight", 70),
            height=u.get("height", 170),
            gender=u.get("gender", "Male")
        )
        stats = get_model_stats()

    st.session_state.user_data["workout_level"] = level

    colors = {"Beginner": "#00ffe7", "Intermediate": "#ffca28", "Advanced": "#ff6b35"}
    color = colors.get(level, "#00ffe7")
    icons = {"Beginner": "🟢", "Intermediate": "🟡", "Advanced": "🔴"}

    st.markdown(f"""
    <div class="ai-card" style="border-color:{color}33; text-align:center; padding:2rem;">
        <div style="font-size:2.5rem; margin-bottom:0.5rem;">{icons.get(level,'⚡')}</div>
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.5rem;">
            Predicted Training Level
        </div>
        <div style="font-family:'Orbitron',monospace; font-size:2rem; color:{color}; font-weight:900; letter-spacing:3px;">
            {level.upper()}
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.5rem;">
            {WORKOUT_PLANS[level]['description']}
        </div>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Algorithm", "Random Forest")
    c2.metric("Estimators", "200 Trees")
    c3.metric("Accuracy", f"{stats['accuracy']}%")
    c4.metric("Dataset", "Real Kaggle" if stats["real_data"] else "Synthetic")

    if stats["real_data"]:
        st.markdown(f"""
        <div style="background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.2);
                    border-radius:8px; padding:0.8rem 1.2rem; margin:0.5rem 0;">
            <span style="color:#00ffe7; font-size:0.8rem;">
                ✅ Trained on <b>Kaggle Body Performance Dataset</b> —
                {stats['n_samples']:,} real records · Accuracy: <b>{stats['accuracy']}%</b>
            </span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,202,40,0.05); border:1px solid rgba(255,202,40,0.2);
                    border-radius:8px; padding:0.8rem 1.2rem; margin:0.5rem 0;">
            <span style="color:#ffca28; font-size:0.8rem;">
                ⚙️ Using synthetic dataset. Place <b>bodyPerformance.csv</b> in the
                <b>data/</b> folder and restart the app to use real Kaggle data.
            </span>
        </div>
        """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
        Weekly Training Plan
    </div>
    """, unsafe_allow_html=True)

    for day, exercises in WORKOUT_PLANS[level]["days"].items():
        with st.expander(f"📅  {day}"):
            for i, ex in enumerate(exercises):
                st.markdown(f"""
                <div style="display:flex; align-items:center; gap:0.8rem; padding:0.4rem 0;
                            border-bottom:1px solid rgba(0,255,231,0.06);">
                    <span style="color:#00ffe7; font-family:'Orbitron',monospace; font-size:0.7rem;
                                 min-width:1.5rem; opacity:0.6;">{str(i+1).zfill(2)}</span>
                    <span style="color:#c8d8f0; font-size:0.85rem;">{ex}</span>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,255,231,0.04); border:1px solid rgba(0,255,231,0.12);
                border-radius:8px; padding:1rem 1.2rem; margin-top:1rem;">
        <span style="color:#5a7a99; font-size:0.8rem;">
            💡 &nbsp; Consistency is weighted at <b style="color:#00ffe7;">30%</b> of your Fitness Score.
        </span>
    </div>
    """, unsafe_allow_html=True)
