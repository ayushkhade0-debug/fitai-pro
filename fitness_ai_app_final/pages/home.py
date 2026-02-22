import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from models.data_loader import get_dataset_status

def show():
    st.markdown("""
    <div style="padding: 2.5rem 0 1.5rem; text-align:center;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:4px; text-transform:uppercase; margin-bottom:1rem;">
            BSc Data Science · Final Year Project · University of Mumbai
        </div>
        <div class="neon-title">FITAI PRO</div>
        <div style="color:#5a7a99; font-size:0.85rem; letter-spacing:3px; text-transform:uppercase; margin-top:0.5rem;">
            Intelligent Health & Fitness Management System
        </div>
        <div style="margin-top:1.5rem;">
            <span class="tag">Random Forest ML</span>
            <span class="tag">Logistic Regression</span>
            <span class="tag">Real Kaggle Datasets</span>
            <span class="tag">Computer Vision</span>
            <span class="tag">AI Chatbot</span>
            <span class="tag">PDF Export</span>
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Dataset status
    status = get_dataset_status()
    st.markdown("""
    <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.8rem;">
        Dataset Status
    </div>
    """, unsafe_allow_html=True)

    d1, d2, d3 = st.columns(3)
    datasets = [
        (d1, "Body Performance", "bodyPerformance.csv", status["body_performance"],
         "13,393 records · Workout ML model", "#00ffe7"),
        (d2, "Food Nutrition", "nutrition.csv", status["nutrition"],
         "8,800+ foods · Diet recommendations", "#00b8ff"),
        (d3, "Exercise & Calories", "exercise.csv", status["exercise"],
         "Calories burned · Dashboard charts", "#ff6b35"),
    ]
    for col, name, fname, loaded, desc, color in datasets:
        with col:
            st.markdown(f"""
            <div style="background:#0d1526; border:1px solid {'rgba(0,255,231,0.25)' if loaded else 'rgba(90,122,153,0.2)'};
                        border-radius:10px; padding:1rem; text-align:center;">
                <div style="font-size:1.4rem; margin-bottom:0.4rem;">{'✅' if loaded else '📂'}</div>
                <div style="font-family:'Orbitron',monospace; font-size:0.75rem;
                            color:{'#00ffe7' if loaded else '#5a7a99'}; margin-bottom:0.3rem;">{name}</div>
                <div style="color:#5a7a99; font-size:0.7rem;">{desc}</div>
                <div style="color:{'#00ffe7' if loaded else '#ffca28'}; font-size:0.65rem; margin-top:0.4rem;">
                    {'ACTIVE' if loaded else f'Add {fname} to data/'}
                </div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:1.5rem 0;'>", unsafe_allow_html=True)

    # Features
    col1, col2, col3 = st.columns(3)
    features = [
        (col1, "🏋️", "#00ffe7", "AI WORKOUT ENGINE",
         "Random Forest · 200 trees · Body Performance Dataset · Beginner / Intermediate / Advanced"),
        (col2, "⚠️", "#ff6b35", "INJURY RISK MODEL",
         "Logistic Regression · Sleep, Fatigue, Heart Rate · Low / Medium / High Risk"),
        (col3, "🥗", "#00b8ff", "NUTRITION ENGINE",
         "Real food dataset · 8,800+ items · BMR-based calorie targets · Food search"),
    ]
    for col, icon, color, title, desc in features:
        with col:
            st.markdown(f"""
            <div class="ai-card">
                <div style="color:{color}; font-size:1.8rem; margin-bottom:0.8rem;">{icon}</div>
                <div style="font-family:'Orbitron',monospace; font-size:0.82rem; color:white;
                            letter-spacing:1px; margin-bottom:0.5rem;">{title}</div>
                <div style="color:#5a7a99; font-size:0.8rem; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)
    col4, col5, col6 = st.columns(3)
    features2 = [
        (col4, "🤖", "#9b59b6", "FITBOT CHATBOT",
         "Rule-based NLP · Hinglish support · Answers workout, diet & injury questions"),
        (col5, "🎥", "#00ffe7", "CV REP COUNTER",
         "MediaPipe pose estimation · 33 landmarks · Squat & Push-up counter via webcam"),
        (col6, "📄", "#ff6b35", "PDF REPORT",
         "One-click export · BMI, Score, Risk, Workout Plan, Diet targets · reportlab"),
    ]
    for col, icon, color, title, desc in features2:
        with col:
            st.markdown(f"""
            <div class="ai-card">
                <div style="color:{color}; font-size:1.8rem; margin-bottom:0.8rem;">{icon}</div>
                <div style="font-family:'Orbitron',monospace; font-size:0.82rem; color:white;
                            letter-spacing:1px; margin-bottom:0.5rem;">{title}</div>
                <div style="color:#5a7a99; font-size:0.8rem; line-height:1.6;">{desc}</div>
            </div>
            """, unsafe_allow_html=True)

    st.markdown("""
    <div style="background:rgba(0,255,231,0.04); border:1px solid rgba(0,255,231,0.12);
                border-radius:10px; padding:1.2rem 1.5rem; text-align:center; margin-top:1rem;">
        <span style="color:#5a7a99; font-size:0.8rem; letter-spacing:2px; text-transform:uppercase;">
            ⚡ &nbsp; Click <b style="color:#00ffe7;">👤 Profile</b> in the sidebar to begin your assessment
        </span>
    </div>
    """, unsafe_allow_html=True)
