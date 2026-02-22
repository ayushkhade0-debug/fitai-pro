import streamlit as st

def calculate_bmi(weight_kg, height_cm):
    h = height_cm / 100
    return round(weight_kg / (h ** 2), 1)

def bmi_category(bmi):
    if bmi < 18.5: return "Underweight", "#4fc3f7"
    elif bmi < 25: return "Normal Weight", "#00ffe7"
    elif bmi < 30: return "Overweight", "#ffca28"
    else: return "Obese", "#ff5252"

def calculate_bmr(weight, height, age, gender):
    if gender == "Male":
        return round(10 * weight + 6.25 * height - 5 * age + 5)
    return round(10 * weight + 6.25 * height - 5 * age - 161)

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 01</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            USER PROFILE & BIOMETRICS
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Enter your details to generate a personalised health baseline
        </div>
    </div>
    """, unsafe_allow_html=True)

    with st.form("profile_form"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Full Name", placeholder="e.g. Ayush Khade")
            age = st.number_input("Age (years)", 10, 100, 21)
            gender = st.selectbox("Biological Sex", ["Male", "Female"])
            weight = st.number_input("Body Weight (kg)", 30.0, 300.0, 70.0, 0.5)
        with col2:
            height = st.number_input("Height (cm)", 100.0, 250.0, 170.0, 0.5)
            goal = st.selectbox("Primary Goal", [
                "Weight Loss", "Muscle Gain", "Maintain Fitness",
                "Improve Endurance", "General Health"
            ])
            activity_level = st.selectbox("Activity Level", [
                "Sedentary (desk job, no exercise)",
                "Lightly Active (1-3 days/week)",
                "Moderately Active (3-5 days/week)",
                "Very Active (6-7 days/week)",
                "Athlete (2x/day training)"
            ])
            experience = st.selectbox("Training Experience", ["Beginner", "Intermediate", "Advanced"])

        submitted = st.form_submit_button("⚡  CALCULATE & SAVE PROFILE")

    if submitted:
        if not name:
            st.error("Please enter your name.")
            return

        bmi = calculate_bmi(weight, height)
        bmi_cat, bmi_color = bmi_category(bmi)
        bmr = calculate_bmr(weight, height, age, gender)
        multipliers = {
            "Sedentary (desk job, no exercise)": 1.2,
            "Lightly Active (1-3 days/week)": 1.375,
            "Moderately Active (3-5 days/week)": 1.55,
            "Very Active (6-7 days/week)": 1.725,
            "Athlete (2x/day training)": 1.9
        }
        tdee = round(bmr * multipliers[activity_level])

        st.session_state.user_data = {
            "name": name, "age": age, "gender": gender,
            "weight": weight, "height": height, "goal": goal,
            "activity_level": activity_level, "fitness_experience": experience,
            "bmi": bmi, "bmi_category": bmi_cat, "bmr": bmr, "tdee": tdee,
        }

        st.markdown("<br>", unsafe_allow_html=True)
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
            Biometric Results
        </div>
        """, unsafe_allow_html=True)

        c1, c2, c3, c4 = st.columns(4)
        c1.metric("BMI Score", bmi)
        c2.metric("BMI Status", bmi_cat)
        c3.metric("BMR (kcal)", bmr)
        c4.metric("TDEE (kcal)", tdee)

        st.markdown("<br>", unsafe_allow_html=True)

        # BMI visual bar
        bmi_pct = min(max((bmi - 10) / 30 * 100, 0), 100)
        st.markdown(f"""
        <div class="ai-card">
            <div style="display:flex; justify-content:space-between; margin-bottom:0.8rem;">
                <div>
                    <div class="stat-label">BMI Analysis</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1.8rem; color:{bmi_color};">{bmi}</div>
                </div>
                <div style="text-align:right;">
                    <div class="stat-label">Classification</div>
                    <div style="font-family:'Orbitron',monospace; font-size:1rem; color:{bmi_color};">{bmi_cat.upper()}</div>
                </div>
            </div>
            <div style="background:#111d35; border-radius:4px; height:6px; overflow:hidden;">
                <div style="width:{bmi_pct}%; height:100%; background:linear-gradient(90deg, #00ffe7, {bmi_color}); border-radius:4px;"></div>
            </div>
            <div style="display:flex; justify-content:space-between; margin-top:0.4rem;">
                <span style="color:#5a7a99; font-size:0.7rem;">Underweight &lt;18.5</span>
                <span style="color:#5a7a99; font-size:0.7rem;">Normal 18.5–24.9</span>
                <span style="color:#5a7a99; font-size:0.7rem;">Obese &gt;30</span>
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.markdown(f"""
        <div style="background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.15);
                    border-radius:8px; padding:1rem; margin-top:0.5rem;">
            <span style="color:#5a7a99; font-size:0.75rem; letter-spacing:2px; text-transform:uppercase;">
                ✅ &nbsp; Profile saved for <b style="color:#00ffe7;">{name.upper()}</b> — 
                proceed to <b style="color:#00ffe7;">🏋️ Workout Plan</b>
            </span>
        </div>
        """, unsafe_allow_html=True)

    elif st.session_state.user_data:
        u = st.session_state.user_data
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
            Current Profile
        </div>
        """, unsafe_allow_html=True)
        c1, c2, c3, c4 = st.columns(4)
        c1.metric("Name", u.get("name"))
        c2.metric("BMI", u.get("bmi"))
        c3.metric("BMR", f"{u.get('bmr')} kcal")
        c4.metric("TDEE", f"{u.get('tdee')} kcal")
        st.info("Fill the form above and click Save to update your profile.")
