import streamlit as st
import plotly.graph_objects as go

def calculate_fitness_score(bmi, sleep, diet_adherence, workout_consistency):
    bmi_factor = max(0, 100 - abs(bmi - 22.5) * 5)
    sleep_factor = max(0, 100 - abs(sleep - 8) * 12)
    score = (workout_consistency * 0.30 + sleep_factor * 0.20 +
             diet_adherence * 0.20 + bmi_factor * 0.30)
    return round(min(score, 100), 1)

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 05 · Composite Scoring</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            FITNESS SCORE ENGINE
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Weighted formula: Consistency 30% · BMI Factor 30% · Sleep 20% · Diet 20%
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.user_data:
        st.warning("⚠️ Complete Profile Setup first.")
        return

    u = st.session_state.user_data

    with st.form("score_form"):
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
            Today's Metrics
        </div>
        """, unsafe_allow_html=True)
        col1, col2 = st.columns(2)
        with col1:
            sleep = st.slider("😴  Sleep Last Night (hours)", 2.0, 12.0, 7.5, 0.5)
            workout_consistency = st.slider("🏋️  Workout Consistency This Week (%)", 0, 100, 70)
        with col2:
            diet_adherence = st.slider("🥗  Diet Adherence Today (%)", 0, 100, 65)
        submitted = st.form_submit_button("⚡  CALCULATE FITNESS SCORE")

    if submitted:
        bmi = u.get("bmi", 22)
        score = calculate_fitness_score(bmi, sleep, diet_adherence, workout_consistency)
        st.session_state.user_data["fitness_score"] = score

        # Score colour
        if score >= 80: sc = "#00ffe7"; rating = "EXCELLENT"
        elif score >= 60: sc = "#00b8ff"; rating = "GOOD"
        elif score >= 40: sc = "#ffca28"; rating = "FAIR"
        else: sc = "#ff5252"; rating = "NEEDS WORK"

        col1, col2 = st.columns(2)

        with col1:
            # Gauge
            fig = go.Figure(go.Indicator(
                mode="gauge+number",
                value=score,
                domain={"x": [0, 1], "y": [0, 1]},
                number={"font": {"family": "Orbitron", "color": sc, "size": 40}},
                gauge={
                    "axis": {"range": [0, 100], "tickcolor": "#5a7a99",
                             "tickfont": {"color": "#5a7a99", "size": 10}},
                    "bar": {"color": sc, "thickness": 0.25},
                    "bgcolor": "#0d1526",
                    "bordercolor": "#1a2a45",
                    "borderwidth": 1,
                    "steps": [
                        {"range": [0, 40], "color": "#0a1520"},
                        {"range": [40, 70], "color": "#0d1a28"},
                        {"range": [70, 100], "color": "#0f2030"},
                    ],
                }
            ))
            fig.update_layout(
                paper_bgcolor="#0d1526", font={"color": "white"},
                height=280, margin={"t": 30, "b": 10, "l": 20, "r": 20}
            )
            st.plotly_chart(fig, use_container_width=True)

        with col2:
            st.markdown(f"""
            <div style="height:280px; display:flex; flex-direction:column; justify-content:center; padding:1rem;">
                <div class="stat-label">Overall Rating</div>
                <div style="font-family:'Orbitron',monospace; font-size:2rem; color:{sc}; font-weight:900; margin:0.5rem 0;">
                    {rating}
                </div>
                <div style="color:#5a7a99; font-size:0.82rem; line-height:1.8;">
                    Score: <b style="color:{sc};">{score}</b> / 100<br>
                    BMI Factor: <b style="color:#c8d8f0;">{round(max(0,100-abs(bmi-22.5)*5),1)}</b><br>
                    Sleep Quality: <b style="color:#c8d8f0;">{round(max(0,100-abs(sleep-8)*12),1)}</b><br>
                    Diet Score: <b style="color:#c8d8f0;">{diet_adherence}</b><br>
                    Consistency: <b style="color:#c8d8f0;">{workout_consistency}</b>
                </div>
            </div>
            """, unsafe_allow_html=True)

        # Breakdown bars
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin:1rem 0 0.8rem;">
            Score Breakdown
        </div>
        """, unsafe_allow_html=True)

        bmi_f = round(max(0, 100 - abs(bmi - 22.5) * 5), 1)
        sleep_f = round(max(0, 100 - abs(sleep - 8) * 12), 1)

        breakdown = [
            ("Workout Consistency", workout_consistency, 0.30, "#00ffe7"),
            ("BMI Factor", bmi_f, 0.30, "#00b8ff"),
            ("Sleep Quality", sleep_f, 0.20, "#9b59b6"),
            ("Diet Adherence", diet_adherence, 0.20, "#ff6b35"),
        ]
        for label, val, weight, color in breakdown:
            contrib = round(val * weight, 1)
            st.markdown(f"""
            <div style="margin-bottom:0.8rem;">
                <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                    <span style="color:#c8d8f0; font-size:0.8rem;">{label}</span>
                    <span style="color:{color}; font-family:'Orbitron',monospace; font-size:0.72rem;">
                        {val}/100 × {int(weight*100)}% = <b>{contrib} pts</b>
                    </span>
                </div>
                <div style="background:#111d35; border-radius:3px; height:5px;">
                    <div style="width:{val}%; height:100%; background:{color}; border-radius:3px; transition:width 0.5s;"></div>
                </div>
            </div>
            """, unsafe_allow_html=True)
