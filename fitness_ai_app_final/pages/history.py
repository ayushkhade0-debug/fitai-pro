import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api_client import log_workout, get_workout_history, get_workout_stats, delete_workout, check_backend

EXERCISES = [
    "Squat", "Deadlift", "Bench Press", "Pull-ups", "Push-ups",
    "Running", "Cycling", "Walking", "HIIT", "Swimming",
    "Shoulder Press", "Barbell Row", "Lunges", "Plank", "Yoga",
]

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 10 · SQLite Database</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            WORKOUT HISTORY TRACKER
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Log sessions · Track progress · Stored in database via FastAPI backend
        </div>
    </div>
    """, unsafe_allow_html=True)

    if not st.session_state.get("logged_in"):
        st.warning("⚠️ Please login first to track your workouts.")
        return

    if not check_backend():
        st.error("❌ Backend not running. Start it with: `uvicorn main:app --reload` in the backend folder.")
        return

    # ── Stats from backend ────────────────────────────────────────────────────
    stats, ok = get_workout_stats()
    if ok and stats.get("total_sessions", 0) > 0:
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Total Sessions",  stats.get("total_sessions", 0))
        c2.metric("Total Calories",  f"{stats.get('total_calories', 0)} kcal")
        c3.metric("Total Minutes",   f"{stats.get('total_minutes', 0)} min")
        c4.metric("Fav Exercise",    stats.get("favourite_exercise", "—"))

        st.markdown("<br>", unsafe_allow_html=True)

    # ── Log new workout ───────────────────────────────────────────────────────
    st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
    text-transform:uppercase; margin-bottom:0.8rem;">Log Today's Session</div>""",
    unsafe_allow_html=True)

    with st.form("log_workout_form"):
        col1, col2 = st.columns(2)
        with col1:
            exercise = st.selectbox("🏋️ Exercise", EXERCISES)
            duration = st.number_input("⏱️ Duration (minutes)", 1, 300, 30)
            calories = st.number_input("🔥 Calories Burned", 0.0, 2000.0, 200.0, 10.0)
        with col2:
            sets  = st.number_input("Sets", 1, 20, 3)
            reps  = st.number_input("Reps per Set", 1, 100, 10)
            notes = st.text_area("Notes (optional)", placeholder="e.g. Felt strong today!", height=100)
        submitted = st.form_submit_button("💾  SAVE WORKOUT")

    if submitted:
        payload = {
            "exercise": exercise, "duration": duration,
            "calories": calories, "sets": sets,
            "reps": reps, "notes": notes
        }
        result, ok = log_workout(payload)
        if ok:
            st.success(f"✅ {exercise} session saved to database!")
            st.rerun()
        else:
            st.error("Failed to save workout. Is the backend running?")

    # ── Workout history from database ─────────────────────────────────────────
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
    text-transform:uppercase; margin-bottom:0.8rem;">Recent Sessions (from Database)</div>""",
    unsafe_allow_html=True)

    history, ok = get_workout_history()
    if ok and history:
        for entry in history:
            col1, col2 = st.columns([5, 1])
            with col1:
                st.markdown(f"""
                <div style="background:#0d1526; border:1px solid rgba(0,255,231,0.12);
                            border-radius:8px; padding:0.9rem 1.2rem; margin-bottom:0.5rem;
                            border-left:3px solid #00ffe7;">
                    <div style="display:flex; justify-content:space-between; margin-bottom:0.3rem;">
                        <span style="color:white; font-family:'Orbitron',monospace; font-size:0.85rem;">
                            {entry['exercise']}
                        </span>
                        <span style="color:#5a7a99; font-size:0.72rem;">
                            {entry['logged_at'][:10]}
                        </span>
                    </div>
                    <div style="color:#5a7a99; font-size:0.78rem;">
                        ⏱️ {entry['duration']} min &nbsp;·&nbsp;
                        🔥 {entry['calories']} kcal &nbsp;·&nbsp;
                        💪 {entry['sets']} sets × {entry['reps']} reps
                        {"&nbsp;·&nbsp; 📝 " + entry['notes'] if entry.get('notes') else ""}
                    </div>
                </div>
                """, unsafe_allow_html=True)
            with col2:
                if st.button("🗑️", key=f"del_{entry['id']}"):
                    delete_workout(entry["id"])
                    st.rerun()
    elif ok:
        st.markdown("""
        <div style="text-align:center; color:#5a7a99; padding:2rem;">
            No workouts logged yet. Log your first session above! 💪
        </div>
        """, unsafe_allow_html=True)
    else:
        st.error("Could not load history. Is the backend running?")
