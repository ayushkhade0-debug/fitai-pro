import streamlit as st
import re
from datetime import datetime

# ── Rule-based fitness knowledge base ──────────────────────────────────────
RESPONSES = {
    # Greetings
    "hello|hi|hey|hlo|helo": [
        "Hey! 👋 I'm FitBot, your AI fitness coach. Ask me anything about workouts, diet, weight loss, or injuries!",
        "Hi there! 💪 What fitness question can I help you with today?",
    ],
    "how are you|how r u|wassup|what's up": [
        "I'm fully charged and ready to help you crush your fitness goals! 🔥 What do you need?",
    ],

    # Weight loss
    "weight loss|lose weight|slim|fat loss|motapa|wajan kam": [
        "🔥 **Weight Loss Tips:**\n\n"
        "• Create a **calorie deficit** of 300–500 kcal/day\n"
        "• Eat **high protein** (1.6–2g per kg of bodyweight)\n"
        "• Do **cardio 3–4x/week** (walking, cycling, HIIT)\n"
        "• **Sleep 7–9 hours** — poor sleep increases hunger hormones\n"
        "• Drink **2.5–3L water** daily\n\n"
        "Your FitAI profile already shows your calorie target — check the 🥗 Diet page!",
    ],

    # Muscle gain
    "muscle|gain|bulk|mass|strength|muscles|body banana": [
        "💪 **Muscle Gain Guide:**\n\n"
        "• Eat in a **calorie surplus** of +200–300 kcal\n"
        "• Protein target: **1.8–2.2g per kg** bodyweight\n"
        "• Train with **progressive overload** — add weight each week\n"
        "• Focus on compound lifts: Squat, Deadlift, Bench Press, Rows\n"
        "• Rest **48 hours** between same muscle groups\n"
        "• Sleep is when muscles GROW — aim for 8 hours! 😴",
    ],

    # Protein
    "protein|protien|whey|egg": [
        "🥩 **Protein Intake Guide:**\n\n"
        "• **Weight loss:** 1.6–2g per kg bodyweight\n"
        "• **Muscle gain:** 1.8–2.2g per kg bodyweight\n"
        "• **Best sources:** Eggs, chicken, paneer, dal, fish, Greek yoghurt, whey\n"
        "• Spread protein across **4–5 meals** for best absorption\n\n"
        "Example: 70kg person building muscle → needs ~140–154g protein/day 💡",
    ],

    # BMI
    "bmi|body mass|weight height": [
        "📊 **BMI (Body Mass Index):**\n\n"
        "• **Formula:** Weight(kg) ÷ Height(m)²\n"
        "• Under 18.5 → Underweight\n"
        "• 18.5–24.9 → Normal ✅\n"
        "• 25–29.9 → Overweight\n"
        "• 30+ → Obese\n\n"
        "Go to 👤 **Profile** page to see your calculated BMI!",
    ],

    # BMR
    "bmr|metabolism|metabolic rate|tdee|calories burn": [
        "🔬 **BMR (Basal Metabolic Rate):**\n\n"
        "This is the calories your body burns at complete rest.\n"
        "Calculated using the **Mifflin-St Jeor Equation**:\n\n"
        "• Males: (10×W) + (6.25×H) − (5×A) + 5\n"
        "• Females: (10×W) + (6.25×H) − (5×A) − 161\n\n"
        "**TDEE** = BMR × Activity Multiplier\n"
        "Check your exact values on the 👤 Profile page!",
    ],

    # Workout
    "workout|exercise|gym|training|begin|start|routine": [
        "🏋️ **Getting Started with Workouts:**\n\n"
        "• **Beginner:** 3 days/week full body (squats, push-ups, rows)\n"
        "• **Intermediate:** 4 days/week upper/lower split\n"
        "• **Advanced:** 5–6 days/week PPL or bro-split\n\n"
        "Always warm up for 5–10 mins before training!\n"
        "Your AI-predicted level is on the 🏋️ **Workout** page 💡",
    ],

    # Cardio
    "cardio|running|jogging|cycling|swimming|walk": [
        "🏃 **Cardio Guide:**\n\n"
        "• **LISS** (Low Intensity): Walking, cycling — good for fat loss & recovery\n"
        "• **HIIT** (High Intensity): 20–30 min, burns more calories in less time\n"
        "• Aim for **150–300 mins** of moderate cardio per week (WHO recommendation)\n"
        "• Don't do heavy cardio on leg day — it affects recovery!",
    ],

    # Sleep
    "sleep|rest|recovery|sona|neend": [
        "😴 **Sleep & Recovery:**\n\n"
        "• Adults need **7–9 hours** per night\n"
        "• Sleep is when your muscles **repair and grow**\n"
        "• Poor sleep raises **cortisol** (stress hormone) → increases fat storage\n"
        "• Poor sleep also increases **ghrelin** (hunger hormone)\n"
        "• Avoid screens 30 mins before bed for better sleep quality\n\n"
        "Sleep is weighted at 20% of your Fitness Score! Check 📊 Score page.",
    ],

    # Injury
    "injury|pain|hurt|sore|knee|back|shoulder|injured": [
        "⚠️ **Injury Advice:**\n\n"
        "• **RICE Method:** Rest, Ice, Compression, Elevation\n"
        "• Don't train through sharp pain — discomfort is ok, pain is not\n"
        "• Allow **48–72 hours** rest for minor muscle soreness\n"
        "• See a **physiotherapist** for joint pain or injuries lasting 7+ days\n\n"
        "Check your injury risk on the ⚠️ **Injury Risk** page!\n\n"
        "⚠️ *This is general information. Always consult a medical professional for injuries.*",
    ],

    # Diet / food
    "diet|food|eat|meal|nutrition|khaana|khana": [
        "🥗 **Diet Basics:**\n\n"
        "• **Eat whole foods** — vegetables, lean protein, complex carbs, healthy fats\n"
        "• Avoid ultra-processed foods, sugary drinks, excess salt\n"
        "• Don't skip meals — it slows metabolism\n"
        "• Eat **every 3–4 hours** to maintain energy levels\n\n"
        "Your personalised meal plan is on the 🥗 **Diet** page!",
    ],

    # Water
    "water|hydration|hydrate|pani": [
        "💧 **Hydration Guide:**\n\n"
        "• Drink **0.033L per kg bodyweight** daily\n"
        "• Example: 70kg person → 2.3L/day\n"
        "• Drink **500ml water** before workouts\n"
        "• Signs of dehydration: dark urine, headaches, fatigue\n"
        "• Coffee and tea count but don't replace plain water!",
    ],

    # Supplements
    "supplement|creatine|whey protein|vitamin|bcaa": [
        "💊 **Supplements (Evidence-Based):**\n\n"
        "• **Creatine Monohydrate** — most researched supplement, improves strength ✅\n"
        "• **Whey Protein** — convenient protein source, not magic ✅\n"
        "• **Vitamin D** — most Indians are deficient, important for health ✅\n"
        "• **Caffeine** — proven pre-workout performance booster ✅\n"
        "• **BCAAs** — not necessary if protein intake is sufficient ❌\n\n"
        "⚠️ Consult a doctor before starting any supplements.",
    ],

    # Motivation
    "motivat|lazy|give up|not working|progress slow|bored": [
        "🔥 **Motivation Boost:**\n\n"
        "• Progress takes time — **trust the process**\n"
        "• Take progress photos every 4 weeks — the mirror lies\n"
        "• Focus on **performance goals** (lift more, run faster) not just weight\n"
        "• Find a **workout partner** for accountability\n"
        "• Remember: **Consistency > Perfection** 💪\n\n"
        "Even 3 workouts/week for 6 months will transform your body!",
    ],

    # Random Forest / ML
    "random forest|machine learning|ml|algorithm|model|logistic": [
        "🤖 **About FitAI's ML Models:**\n\n"
        "• **Workout Recommendation** uses **Random Forest** (100 decision trees)\n"
        "  → Inputs: Age, BMI, Experience, Goal, Activity Level\n"
        "  → Output: Beginner / Intermediate / Advanced\n\n"
        "• **Injury Risk** uses **Logistic Regression** (multinomial)\n"
        "  → Inputs: Sleep, Fatigue, Heart Rate, Workout Frequency\n"
        "  → Output: Low / Medium / High Risk\n\n"
        "Both models are trained using **scikit-learn** on synthetic datasets.",
    ],

    # Thanks
    "thank|thanks|thnx|thx|shukriya": [
        "You're welcome! 😊 Keep pushing — consistency is everything! 💪",
        "Anytime! 🙌 Stay consistent and results will follow!",
    ],

    # Bye
    "bye|goodbye|cya|see you|tata": [
        "Goodbye! 💪 Stay consistent and keep crushing those goals! 🔥",
    ],
}

def get_response(user_input: str) -> str:
    text = user_input.lower().strip()

    for pattern, replies in RESPONSES.items():
        if re.search(pattern, text):
            import random
            return random.choice(replies)

    # Check if user mentions their profile data
    if st.session_state.user_data:
        u = st.session_state.user_data
        if any(w in text for w in ["my bmi", "my weight", "my score", "my calories", "my plan"]):
            return (
                f"📊 **Your Current Stats:**\n\n"
                f"• **Name:** {u.get('name','—')}\n"
                f"• **BMI:** {u.get('bmi','—')} ({u.get('bmi_category','—')})\n"
                f"• **BMR:** {u.get('bmr','—')} kcal/day\n"
                f"• **TDEE:** {u.get('tdee','—')} kcal/day\n"
                f"• **Goal:** {u.get('goal','—')}\n"
                f"• **Workout Level:** {u.get('workout_level','Not set yet')}\n"
                f"• **Fitness Score:** {u.get('fitness_score','Not calculated yet')}/100\n"
                f"• **Injury Risk:** {u.get('injury_risk','Not assessed yet')}\n\n"
                f"Go through each page in the sidebar to complete your assessment! 💡"
            )

    return (
        "🤔 I'm not sure about that specific question, but I can help with:\n\n"
        "• **Weight loss / muscle gain** tips\n"
        "• **Diet & nutrition** advice\n"
        "• **Workout** recommendations\n"
        "• **Sleep & recovery** guidance\n"
        "• **Injury** prevention\n"
        "• **Supplements** info\n"
        "• Your **personal stats** (type 'my bmi' or 'my plan')\n\n"
        "Try asking something like: *'How do I lose weight?'* or *'What should I eat?'*"
    )


def show():
    st.markdown("""
    <div style="margin-bottom:2rem;">
        <div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px; text-transform:uppercase;">Module 08 · NLP Chatbot</div>
        <div style="font-family:'Orbitron',monospace; font-size:1.5rem; color:white; font-weight:700; margin-top:0.3rem;">
            FITBOT — AI FITNESS COACH
        </div>
        <div style="color:#5a7a99; font-size:0.82rem; margin-top:0.3rem;">
            Ask anything about workouts, diet, weight loss, injuries, or your personal stats
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Init chat history
    if "chat_history" not in st.session_state:
        st.session_state.chat_history = [
            {
                "role": "bot",
                "text": "👋 Hey! I'm **FitBot**, your AI fitness coach.\n\nAsk me anything — workouts, diet, weight loss, injuries, supplements, or type **'my stats'** to see your personal data!\n\n*I also understand Hinglish — try 'motapa kaise kam kare?' 😄*",
                "time": datetime.now().strftime("%H:%M")
            }
        ]

    # Chat display
    chat_container = st.container()
    with chat_container:
        for msg in st.session_state.chat_history:
            if msg["role"] == "bot":
                st.markdown(f"""
                <div style="display:flex; gap:0.8rem; margin-bottom:1rem; align-items:flex-start;">
                    <div style="background:linear-gradient(135deg,#00ffe7,#00b8ff); border-radius:50%;
                                width:36px; height:36px; display:flex; align-items:center;
                                justify-content:center; font-size:1rem; flex-shrink:0;">🤖</div>
                    <div style="background:#0d1526; border:1px solid rgba(0,255,231,0.15);
                                border-radius:0 12px 12px 12px; padding:0.9rem 1.1rem;
                                max-width:85%; color:#c8d8f0; font-size:0.85rem; line-height:1.7;">
                        {msg['text'].replace(chr(10), '<br>')}
                        <div style="color:#5a7a99; font-size:0.68rem; margin-top:0.5rem;">{msg['time']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
            else:
                st.markdown(f"""
                <div style="display:flex; gap:0.8rem; margin-bottom:1rem; align-items:flex-start; flex-direction:row-reverse;">
                    <div style="background:#1a2a45; border-radius:50%;
                                width:36px; height:36px; display:flex; align-items:center;
                                justify-content:center; font-size:1rem; flex-shrink:0;">👤</div>
                    <div style="background:#111d35; border:1px solid rgba(0,184,255,0.15);
                                border-radius:12px 0 12px 12px; padding:0.9rem 1.1rem;
                                max-width:85%; color:#c8d8f0; font-size:0.85rem; line-height:1.7;">
                        {msg['text']}
                        <div style="color:#5a7a99; font-size:0.68rem; margin-top:0.5rem;">{msg['time']}</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)

    st.markdown("<br>", unsafe_allow_html=True)

    # Quick suggestion buttons
    st.markdown("""
    <div style="color:#5a7a99; font-size:0.68rem; letter-spacing:2px; text-transform:uppercase; margin-bottom:0.5rem;">
        Quick Questions
    </div>
    """, unsafe_allow_html=True)

    suggestions = [
        "How do I lose weight?",
        "Best foods for muscle gain?",
        "How much protein do I need?",
        "My stats",
        "I feel lazy to workout",
        "How much water should I drink?",
    ]

    cols = st.columns(3)
    for i, suggestion in enumerate(suggestions):
        with cols[i % 3]:
            if st.button(suggestion, key=f"suggest_{i}"):
                # Add user message
                st.session_state.chat_history.append({
                    "role": "user",
                    "text": suggestion,
                    "time": datetime.now().strftime("%H:%M")
                })
                # Add bot response
                response = get_response(suggestion)
                st.session_state.chat_history.append({
                    "role": "bot",
                    "text": response,
                    "time": datetime.now().strftime("%H:%M")
                })
                st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)

    # Input box
    with st.form("chat_form", clear_on_submit=True):
        col1, col2 = st.columns([5, 1])
        with col1:
            user_input = st.text_input(
                "Message",
                placeholder="Ask FitBot anything... (e.g. 'How do I build muscle?' or 'motapa kaise kam kare?')",
                label_visibility="collapsed"
            )
        with col2:
            send = st.form_submit_button("⚡ Send")

    if send and user_input.strip():
        st.session_state.chat_history.append({
            "role": "user",
            "text": user_input,
            "time": datetime.now().strftime("%H:%M")
        })
        response = get_response(user_input)
        st.session_state.chat_history.append({
            "role": "bot",
            "text": response,
            "time": datetime.now().strftime("%H:%M")
        })
        st.rerun()

    # Clear chat
    if len(st.session_state.chat_history) > 2:
        if st.button("🗑️ Clear Chat"):
            st.session_state.chat_history = [st.session_state.chat_history[0]]
            st.rerun()
