import streamlit as st
import plotly.graph_objects as go
import numpy as np
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.data_loader import exercise_load, get_dataset_status

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 06 · Live Analytics</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            PERFORMANCE DASHBOARD
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Real-time visualisation powered by real exercise & nutrition datasets
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.user_data:
        st.warning("⚠️ Complete Profile Setup first.")
        return

    u = st.session_state.user_data

    # Dataset status banner
    status = get_dataset_status()
    loaded = status["count"]
    st.markdown(f"""
    <div style="background:rgba(0,255,231,0.04); border:1px solid rgba(0,255,231,0.12);
                border-radius:8px; padding:0.8rem 1.2rem; margin-bottom:1.5rem;
                display:flex; gap:2rem; align-items:center;">
        <span style="color:#5a7a99; font-size:0.72rem; letter-spacing:2px; text-transform:uppercase;">Datasets Active</span>
        <span style="color:{'#00ffe7' if status['body_performance'] else '#5a7a99'}; font-size:0.8rem;">
            {'✅' if status['body_performance'] else '⚙️'} Body Performance
        </span>
        <span style="color:{'#00ffe7' if status['nutrition'] else '#5a7a99'}; font-size:0.8rem;">
            {'✅' if status['nutrition'] else '⚙️'} Nutrition
        </span>
        <span style="color:{'#00ffe7' if status['exercise'] else '#5a7a99'}; font-size:0.8rem;">
            {'✅' if status['exercise'] else '⚙️'} Exercise
        </span>
        <span style="color:#00ffe7; font-family:'Orbitron',monospace; font-size:0.75rem; margin-left:auto;">
            {loaded}/3 LOADED
        </span>
    </div>
    """, unsafe_allow_html=True)

    # Top KPIs
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("BMI", u.get("bmi", "—"), u.get("bmi_category", ""))
    c2.metric("Fitness Score", f"{u.get('fitness_score', '—')}/100")
    c3.metric("Injury Risk", u.get("injury_risk", "—"))
    c4.metric("Daily Calories", f"{u.get('tdee', '—')} kcal")

    st.markdown("<br>", unsafe_allow_html=True)

    PLOT_BG = "#070b14"
    SURFACE = "#0d1526"
    GRID    = "#1a2a45"
    days    = ["Mon", "Tue", "Wed", "Thu", "Fri", "Sat", "Sun"]
    np.random.seed(42)

    # ── Load exercise dataset for calorie chart ───────────────────────────────
    ex_df, ex_real = exercise_load()

    if ex_real and ex_df is not None and "calories" in ex_df.columns:
        # Sample 7 rows to simulate a week
        sample = ex_df.sample(min(7, len(ex_df)), random_state=42)
        cal_burned = sample["calories"].astype(int).tolist()
        while len(cal_burned) < 7:
            cal_burned.append(int(ex_df["calories"].mean()))
        cal_burned = cal_burned[:7]
        cal_source = "Real Exercise Dataset"
    else:
        base = u.get("tdee", 2000)
        cal_burned = [int(base * x) for x in np.random.uniform(0.3, 0.65, 7)]
        cal_source = "Estimated"

    # Calories bar chart
    fig1 = go.Figure()
    avg = np.mean(cal_burned)
    fig1.add_trace(go.Bar(
        x=days, y=cal_burned,
        marker=dict(color=["#00ffe7" if c >= avg else "#1a2a45" for c in cal_burned]),
        hovertemplate="<b>%{x}</b><br>%{y} kcal<extra></extra>"
    ))
    fig1.add_hline(y=avg, line_dash="dot", line_color="#ff6b35",
                   annotation_text=f"Avg: {int(avg)} kcal", annotation_font_color="#ff6b35",
                   annotation_font_size=10)
    fig1.update_layout(
        title=dict(text=f"Calories Burned This Week ({cal_source})",
                   font=dict(family="Orbitron", color="white", size=12)),
        paper_bgcolor=PLOT_BG, plot_bgcolor=SURFACE,
        font=dict(color="#5a7a99"),
        xaxis=dict(gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        yaxis=dict(gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        height=270, margin=dict(t=40, b=20, l=20, r=20)
    )

    # Sleep chart
    sleep_data = np.random.uniform(5.5, 9, 7).round(1)
    fig2 = go.Figure()
    fig2.add_trace(go.Scatter(
        x=days, y=sleep_data,
        mode="lines+markers",
        line=dict(color="#9b59b6", width=2.5),
        marker=dict(size=8, color="#9b59b6", line=dict(color="#070b14", width=2)),
        fill="tozeroy", fillcolor="rgba(155,89,182,0.08)",
        hovertemplate="<b>%{x}</b><br>%{y}h sleep<extra></extra>"
    ))
    fig2.add_hline(y=8, line_dash="dot", line_color="#00ffe7",
                   annotation_text="Ideal: 8h", annotation_font_color="#00ffe7",
                   annotation_font_size=10)
    fig2.update_layout(
        title=dict(text="Sleep Tracking", font=dict(family="Orbitron", color="white", size=12)),
        paper_bgcolor=PLOT_BG, plot_bgcolor=SURFACE, font=dict(color="#5a7a99"),
        xaxis=dict(gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        yaxis=dict(range=[3, 11], gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        height=270, margin=dict(t=40, b=20, l=20, r=20)
    )

    col1, col2 = st.columns(2)
    with col1: st.plotly_chart(fig1, use_container_width=True)
    with col2: st.plotly_chart(fig2, use_container_width=True)

    # Macros donut
    diet_cal = u.get("diet_calories", 2000)
    fig3 = go.Figure(go.Pie(
        labels=["Protein", "Carbohydrates", "Fats"],
        values=[diet_cal * 0.35 / 4, diet_cal * 0.40 / 4, diet_cal * 0.25 / 9],
        hole=0.65,
        marker=dict(colors=["#00ffe7", "#00b8ff", "#ff6b35"],
                    line=dict(color=PLOT_BG, width=3)),
        hovertemplate="<b>%{label}</b><br>%{value:.0f}g<br>%{percent}<extra></extra>",
        textfont=dict(color="white", size=11)
    ))
    fig3.add_annotation(text="MACROS", x=0.5, y=0.55,
                        font=dict(family="Orbitron", color="#5a7a99", size=10), showarrow=False)
    fig3.add_annotation(text=f"{diet_cal}", x=0.5, y=0.45,
                        font=dict(family="Orbitron", color="#00ffe7", size=18), showarrow=False)
    fig3.add_annotation(text="kcal", x=0.5, y=0.35,
                        font=dict(color="#5a7a99", size=10), showarrow=False)
    fig3.update_layout(
        title=dict(text="Macro Distribution", font=dict(family="Orbitron", color="white", size=12)),
        paper_bgcolor=PLOT_BG, font=dict(color="#5a7a99"),
        height=300, margin=dict(t=40, b=20, l=20, r=20),
        showlegend=True, legend=dict(font=dict(color="#c8d8f0"), bgcolor="rgba(0,0,0,0)")
    )

    # Score trend
    score = u.get("fitness_score", 55)
    weeks = ["Week 1", "Week 2", "Week 3", "Week 4", "Now"]
    scores = [max(20, score-20), max(28, score-14), max(35, score-8), max(40, score-3), score]
    fig4 = go.Figure()
    fig4.add_trace(go.Scatter(
        x=weeks, y=scores,
        mode="lines+markers",
        line=dict(color="#00ffe7", width=3),
        marker=dict(size=10, color="#00ffe7", line=dict(color="#070b14", width=2)),
        fill="tozeroy", fillcolor="rgba(0,255,231,0.06)",
        hovertemplate="<b>%{x}</b><br>Score: %{y}<extra></extra>"
    ))
    fig4.update_layout(
        title=dict(text="Fitness Score Trend", font=dict(family="Orbitron", color="white", size=12)),
        paper_bgcolor=PLOT_BG, plot_bgcolor=SURFACE, font=dict(color="#5a7a99"),
        xaxis=dict(gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        yaxis=dict(range=[0, 105], gridcolor=GRID, tickfont=dict(color="#5a7a99")),
        height=300, margin=dict(t=40, b=20, l=20, r=20)
    )

    col3, col4 = st.columns(2)
    with col3: st.plotly_chart(fig3, use_container_width=True)
    with col4: st.plotly_chart(fig4, use_container_width=True)

    # ── Exercise stats from real dataset ─────────────────────────────────────
    if ex_real and ex_df is not None:
        st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
        text-transform:uppercase; margin:1rem 0 0.8rem;">Real Dataset Insights</div>""",
        unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Dataset Records", f"{len(ex_df):,}")
        c2.metric("Avg Calories Burned", f"{int(ex_df['calories'].mean())} kcal")
        if "duration" in ex_df.columns:
            c3.metric("Avg Duration", f"{int(ex_df['duration'].mean())} min")
        if "heart_rate" in ex_df.columns:
            c4.metric("Avg Heart Rate", f"{int(ex_df['heart_rate'].mean())} bpm")
