import streamlit as st
import numpy as np
import math

def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 09 · Computer Vision · MediaPipe</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            EXERCISE REP COUNTER
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Real-time pose estimation using MediaPipe — counts Squats & Push-ups via webcam
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Check if mediapipe is available
    try:
        import mediapipe as mp
        import cv2
        HAS_CV = True
    except ImportError:
        HAS_CV = False

    if not HAS_CV:
        st.markdown("""
        <div class="ai-card" style="border-color:#ff6b3544; text-align:center; padding:2rem;">
            <div style="font-size:2rem; margin-bottom:0.8rem;">📦</div>
            <div style="font-family:'Orbitron',monospace; color:#ff6b35; font-size:1rem; margin-bottom:0.5rem;">
                INSTALL REQUIRED LIBRARIES
            </div>
            <div style="color:#5a7a99; font-size:0.85rem; margin-bottom:1.5rem;">
                This module needs OpenCV and MediaPipe. Run this in your VS Code terminal:
            </div>
        </div>
        """, unsafe_allow_html=True)

        st.code("py -m pip install opencv-python mediapipe", language="bash")

        st.markdown("""
        <div style="background:rgba(0,255,231,0.04); border:1px solid rgba(0,255,231,0.12);
                    border-radius:8px; padding:1.2rem; margin-top:1rem;">
            <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.5rem;">
                After installing, restart the app:
            </div>
            <code style="color:#00ffe7; font-size:0.85rem;">py -m streamlit run app.py</code>
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Show what it does even without camera
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:1rem;">
            How It Works
        </div>
        """, unsafe_allow_html=True)

        cols = st.columns(3)
        steps = [
            ("📷", "Webcam Capture", "OpenCV captures live video frames from your camera"),
            ("🦴", "Pose Estimation", "MediaPipe detects 33 body landmarks in real-time"),
            ("📐", "Angle Calculation", "Joint angles (hip, knee, elbow) are calculated mathematically"),
        ]
        for col, (icon, title, desc) in zip(cols, steps):
            with col:
                st.markdown(f"""
                <div class="ai-card" style="text-align:center;">
                    <div style="font-size:1.8rem; margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:white; margin-bottom:0.4rem;">{title}</div>
                    <div style="color:#5a7a99; font-size:0.78rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        cols2 = st.columns(3)
        steps2 = [
            ("🔢", "Rep Counting", "When joint angle crosses threshold, a rep is counted automatically"),
            ("⚠️", "Form Feedback", "Bad form (shallow squat, incorrect push-up) triggers alerts"),
            ("📊", "Session Stats", "Total reps, sets, estimated calories shown after workout"),
        ]
        for col, (icon, title, desc) in zip(cols2, steps2):
            with col:
                st.markdown(f"""
                <div class="ai-card" style="text-align:center;">
                    <div style="font-size:1.8rem; margin-bottom:0.5rem;">{icon}</div>
                    <div style="font-family:'Orbitron',monospace; font-size:0.8rem; color:white; margin-bottom:0.4rem;">{title}</div>
                    <div style="color:#5a7a99; font-size:0.78rem;">{desc}</div>
                </div>
                """, unsafe_allow_html=True)

        st.markdown("<br>", unsafe_allow_html=True)

        # Show the angle calculation code as academic content
        st.markdown("""
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.8rem;">
            Pose Estimation Algorithm (MediaPipe + Angle Calculation)
        </div>
        """, unsafe_allow_html=True)

        st.code("""
import mediapipe as mp
import cv2, math

mp_pose = mp.solutions.pose

def calculate_angle(a, b, c):
    \"\"\"Calculate angle at joint b between points a and c\"\"\"
    radians = math.atan2(c[1]-b[1], c[0]-b[0]) - \
              math.atan2(a[1]-b[1], a[0]-b[0])
    angle = abs(math.degrees(radians))
    return 360 - angle if angle > 180 else angle

# Squat rep logic
def count_squat_rep(knee_angle, state):
    if knee_angle < 90 and state == "up":
        return "down"       # went into squat
    elif knee_angle > 160 and state == "down":
        return "up"         # completed rep → count +1
    return state

# Push-up rep logic  
def count_pushup_rep(elbow_angle, state):
    if elbow_angle < 90 and state == "up":
        return "down"       # went down
    elif elbow_angle > 160 and state == "down":
        return "up"         # completed rep → count +1
    return state
        """, language="python")
        return

    # ── LIVE CV MODE (when mediapipe is installed) ──────────────────────
    import cv2
    import mediapipe as mp

    mp_pose = mp.solutions.pose
    mp_draw = mp.solutions.drawing_utils

    def calculate_angle(a, b, c):
        radians = math.atan2(c[1]-b[1], c[0]-b[0]) - math.atan2(a[1]-b[1], a[0]-b[0])
        angle = abs(math.degrees(radians))
        return 360 - angle if angle > 180 else angle

    # Session state
    if "cv_reps" not in st.session_state:
        st.session_state.cv_reps = 0
    if "cv_state" not in st.session_state:
        st.session_state.cv_state = "up"
    if "cv_sets" not in st.session_state:
        st.session_state.cv_sets = 0
    if "cv_running" not in st.session_state:
        st.session_state.cv_running = False

    # Exercise selector
    col1, col2 = st.columns(2)
    with col1:
        exercise = st.selectbox("🏋️  Select Exercise", ["Squat", "Push-up"])
    with col2:
        target_reps = st.number_input("🎯  Target Reps per Set", 5, 50, 10)

    # Stats row
    c1, c2, c3, c4 = st.columns(4)
    c1.metric("Reps", st.session_state.cv_reps)
    c2.metric("Sets", st.session_state.cv_sets)
    c3.metric("Target", target_reps)
    weight = st.session_state.user_data.get("weight", 70) if st.session_state.user_data else 70
    cal_per_rep = 0.32 if exercise == "Squat" else 0.29
    total_reps_all = st.session_state.cv_reps + st.session_state.cv_sets * target_reps
    c4.metric("Est. Calories", f"{round(total_reps_all * cal_per_rep * weight / 70, 1)} kcal")

    col_start, col_stop, col_reset = st.columns(3)
    with col_start:
        if st.button("▶️  START CAMERA"):
            st.session_state.cv_running = True
            st.session_state.cv_reps = 0
            st.session_state.cv_state = "up"
    with col_stop:
        if st.button("⏹️  STOP"):
            st.session_state.cv_running = False
    with col_reset:
        if st.button("🔄  RESET"):
            st.session_state.cv_reps = 0
            st.session_state.cv_sets = 0
            st.session_state.cv_state = "up"

    frame_placeholder = st.empty()
    feedback_placeholder = st.empty()

    if st.session_state.cv_running:
        cap = cv2.VideoCapture(0)

        if not cap.isOpened():
            st.error("❌ Cannot access webcam. Please allow camera access and try again.")
            st.session_state.cv_running = False
            return

        with mp_pose.Pose(min_detection_confidence=0.6, min_tracking_confidence=0.6) as pose:
            while st.session_state.cv_running:
                ret, frame = cap.read()
                if not ret:
                    break

                frame = cv2.flip(frame, 1)
                rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                results = pose.process(rgb)

                angle = None
                feedback = "Position yourself in front of the camera"
                color = (0, 255, 231)

                if results.pose_landmarks:
                    lm = results.pose_landmarks.landmark
                    h, w = frame.shape[:2]

                    def get_point(idx):
                        return [lm[idx].x * w, lm[idx].y * h]

                    if exercise == "Squat":
                        hip = get_point(mp_pose.PoseLandmark.LEFT_HIP.value)
                        knee = get_point(mp_pose.PoseLandmark.LEFT_KNEE.value)
                        ankle = get_point(mp_pose.PoseLandmark.LEFT_ANKLE.value)
                        angle = calculate_angle(hip, knee, ankle)

                        if angle < 90:
                            if st.session_state.cv_state == "up":
                                st.session_state.cv_state = "down"
                            feedback = "✅ Good depth! Now stand up"
                            color = (0, 255, 100)
                        elif angle > 160:
                            if st.session_state.cv_state == "down":
                                st.session_state.cv_reps += 1
                                st.session_state.cv_state = "up"
                                if st.session_state.cv_reps >= target_reps:
                                    st.session_state.cv_sets += 1
                                    st.session_state.cv_reps = 0
                            feedback = "⬇️ Squat down — bend your knees"
                        elif angle < 120:
                            feedback = "⚠️ Go deeper for full range of motion"
                            color = (255, 165, 0)

                    else:  # Push-up
                        shoulder = get_point(mp_pose.PoseLandmark.LEFT_SHOULDER.value)
                        elbow = get_point(mp_pose.PoseLandmark.LEFT_ELBOW.value)
                        wrist = get_point(mp_pose.PoseLandmark.LEFT_WRIST.value)
                        angle = calculate_angle(shoulder, elbow, wrist)

                        if angle < 90:
                            if st.session_state.cv_state == "up":
                                st.session_state.cv_state = "down"
                            feedback = "✅ Good! Now push up"
                            color = (0, 255, 100)
                        elif angle > 160:
                            if st.session_state.cv_state == "down":
                                st.session_state.cv_reps += 1
                                st.session_state.cv_state = "up"
                                if st.session_state.cv_reps >= target_reps:
                                    st.session_state.cv_sets += 1
                                    st.session_state.cv_reps = 0
                            feedback = "⬇️ Lower your chest to the ground"

                    # Draw landmarks
                    mp_draw.draw_landmarks(
                        frame, results.pose_landmarks, mp_pose.POSE_CONNECTIONS,
                        mp_draw.DrawingSpec(color=(0, 255, 231), thickness=2, circle_radius=3),
                        mp_draw.DrawingSpec(color=(255, 107, 53), thickness=2)
                    )

                    # Overlay stats
                    cv2.rectangle(frame, (0, 0), (280, 120), (7, 11, 20), -1)
                    cv2.putText(frame, f"REPS: {st.session_state.cv_reps}", (15, 40),
                                cv2.FONT_HERSHEY_SIMPLEX, 1.2, color, 3)
                    cv2.putText(frame, f"SETS: {st.session_state.cv_sets}", (15, 80),
                                cv2.FONT_HERSHEY_SIMPLEX, 1, (200, 200, 200), 2)
                    if angle:
                        cv2.putText(frame, f"ANGLE: {int(angle)}", (15, 115),
                                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (90, 122, 153), 1)

                frame_placeholder.image(frame, channels="BGR", use_container_width=True)
                feedback_placeholder.markdown(f"""
                <div style="background:#0d1526; border:1px solid rgba(0,255,231,0.2);
                            border-radius:8px; padding:0.8rem 1.2rem; text-align:center; margin-top:0.5rem;">
                    <span style="color:#c8d8f0; font-size:0.9rem;">{feedback}</span>
                </div>
                """, unsafe_allow_html=True)

        cap.release()

    # Instructions
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("""
    <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase; margin-bottom:0.8rem;">
        Instructions
    </div>
    """, unsafe_allow_html=True)

    inst_cols = st.columns(2)
    with inst_cols[0]:
        st.markdown("""
        <div class="ai-card">
            <div style="font-family:'Orbitron',monospace; color:#00ffe7; font-size:0.8rem; margin-bottom:0.8rem;">🦵 SQUAT SETUP</div>
            <div style="color:#c8d8f0; font-size:0.82rem; line-height:1.8;">
                • Stand 1–2 metres from camera<br>
                • Camera should see full body<br>
                • Stand sideways for best accuracy<br>
                • Feet shoulder-width apart<br>
                • Squat until knees are at 90°
            </div>
        </div>
        """, unsafe_allow_html=True)

    with inst_cols[1]:
        st.markdown("""
        <div class="ai-card">
            <div style="font-family:'Orbitron',monospace; color:#ff6b35; font-size:0.8rem; margin-bottom:0.8rem;">💪 PUSH-UP SETUP</div>
            <div style="color:#c8d8f0; font-size:0.82rem; line-height:1.8;">
                • Place camera at floor level<br>
                • Camera should see upper body<br>
                • Position sideways to camera<br>
                • Keep body in straight line<br>
                • Lower chest close to ground
            </div>
        </div>
        """, unsafe_allow_html=True)
