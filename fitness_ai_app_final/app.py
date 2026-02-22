import streamlit as st

st.set_page_config(
    page_title="FitAI Pro — Intelligent Fitness System",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700;900&family=DM+Sans:wght@300;400;500&display=swap');
:root {
    --neon:#00ffe7; --neon2:#ff6b35; --bg:#070b14;
    --surface:#0d1526; --surface2:#111d35;
    --border:rgba(0,255,231,0.15); --text:#c8d8f0; --muted:#5a7a99;
}
html,body,[class*="css"]{background-color:var(--bg)!important;color:var(--text)!important;font-family:'DM Sans',sans-serif!important;}
.stApp{background-image:linear-gradient(rgba(0,255,231,0.03) 1px,transparent 1px),linear-gradient(90deg,rgba(0,255,231,0.03) 1px,transparent 1px);background-size:40px 40px;background-color:var(--bg)!important;}
section[data-testid="stSidebar"]{background:linear-gradient(180deg,#070b14 0%,#0a1020 100%)!important;border-right:1px solid var(--border)!important;}
section[data-testid="stSidebar"] .stButton>button{background:transparent!important;color:var(--muted)!important;border:1px solid transparent!important;border-radius:8px!important;font-family:'DM Sans',sans-serif!important;font-size:0.88rem!important;text-align:left!important;padding:0.55rem 1rem!important;width:100%!important;transition:all 0.2s ease!important;}
section[data-testid="stSidebar"] .stButton>button:hover{background:rgba(0,255,231,0.08)!important;color:var(--neon)!important;border-color:var(--border)!important;}
.main .stButton>button{background:linear-gradient(135deg,#00ffe7,#00b8a9)!important;color:#070b14!important;font-family:'Orbitron',monospace!important;font-weight:700!important;font-size:0.85rem!important;border:none!important;border-radius:6px!important;padding:0.65rem 2rem!important;letter-spacing:1.5px!important;width:100%!important;transition:all 0.3s ease!important;text-transform:uppercase!important;}
.main .stButton>button:hover{transform:translateY(-2px)!important;box-shadow:0 8px 25px rgba(0,255,231,0.3)!important;}
.ai-card{background:var(--surface);border:1px solid var(--border);border-radius:12px;padding:1.5rem;margin-bottom:1rem;position:relative;overflow:hidden;transition:all 0.3s ease;}
.ai-card::before{content:'';position:absolute;top:0;left:0;right:0;height:2px;background:linear-gradient(90deg,transparent,var(--neon),transparent);}
.ai-card:hover{border-color:rgba(0,255,231,0.35);box-shadow:0 0 30px rgba(0,255,231,0.07);}
h1,h2,h3{font-family:'Orbitron',monospace!important;color:white!important;letter-spacing:1px!important;}
[data-testid="metric-container"]{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:10px!important;padding:1rem!important;}
[data-testid="metric-container"] label{color:var(--muted)!important;font-size:0.72rem!important;letter-spacing:1px!important;text-transform:uppercase!important;}
[data-testid="stMetricValue"]{color:var(--neon)!important;font-family:'Orbitron',monospace!important;font-size:1.5rem!important;}
.stTextInput input,.stNumberInput input{background:var(--surface2)!important;border:1px solid var(--border)!important;color:var(--text)!important;border-radius:6px!important;}
[data-testid="stForm"]{background:var(--surface)!important;border:1px solid var(--border)!important;border-radius:12px!important;padding:1.5rem!important;}
.stSuccess{background:rgba(0,255,100,0.08)!important;border:1px solid rgba(0,255,100,0.3)!important;border-radius:8px!important;}
.stWarning{background:rgba(255,170,0,0.08)!important;border:1px solid rgba(255,170,0,0.3)!important;border-radius:8px!important;}
.stError{background:rgba(255,60,60,0.08)!important;border:1px solid rgba(255,60,60,0.3)!important;border-radius:8px!important;}
.stInfo{background:rgba(0,180,255,0.08)!important;border:1px solid rgba(0,180,255,0.25)!important;border-radius:8px!important;}
details{background:var(--surface2)!important;border:1px solid var(--border)!important;border-radius:8px!important;margin-bottom:0.5rem!important;}
::-webkit-scrollbar{width:5px;}
::-webkit-scrollbar-track{background:var(--bg);}
::-webkit-scrollbar-thumb{background:var(--border);border-radius:3px;}
hr{border-color:var(--border)!important;}
.neon-title{font-family:'Orbitron',monospace;font-size:2.4rem;font-weight:900;background:linear-gradient(135deg,#00ffe7,#00b8ff);-webkit-background-clip:text;-webkit-text-fill-color:transparent;background-clip:text;letter-spacing:3px;margin:0;}
.stat-label{color:var(--muted);font-size:0.7rem;letter-spacing:2px;text-transform:uppercase;margin-bottom:0.2rem;}
.tag{display:inline-block;background:rgba(0,255,231,0.1);border:1px solid rgba(0,255,231,0.25);color:var(--neon);font-size:0.7rem;letter-spacing:1.5px;text-transform:uppercase;padding:0.2rem 0.6rem;border-radius:4px;margin-right:0.4rem;margin-bottom:0.4rem;}
</style>
""", unsafe_allow_html=True)

# ── Session state ──────────────────────────────────────────────────────────────
if "user_data"    not in st.session_state: st.session_state.user_data = {}
if "page"         not in st.session_state: st.session_state.page = "Home"
if "chat_history" not in st.session_state: st.session_state.chat_history = []
if "logged_in"    not in st.session_state: st.session_state.logged_in = False
if "token"        not in st.session_state: st.session_state.token = ""
if "username"     not in st.session_state: st.session_state.username = ""

# ── Sidebar ────────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("""
    <div style="padding:1.5rem 0.5rem 1rem;">
        <div style="font-family:'Orbitron',monospace;font-size:1.2rem;font-weight:900;
                    background:linear-gradient(135deg,#00ffe7,#00b8ff);
                    -webkit-background-clip:text;-webkit-text-fill-color:transparent;
                    background-clip:text;letter-spacing:3px;">⚡ FITAI PRO</div>
        <div style="color:#5a7a99;font-size:0.65rem;letter-spacing:2px;text-transform:uppercase;margin-top:0.2rem;">
            Intelligent Fitness System v4.0
        </div>
    </div>
    """, unsafe_allow_html=True)

    st.markdown("<hr style='margin:0 0 0.5rem 0;'>", unsafe_allow_html=True)

    # Auth status
    if st.session_state.logged_in:
        st.markdown(f"""
        <div style="background:rgba(0,255,231,0.05);border:1px solid rgba(0,255,231,0.2);
                    border-radius:8px;padding:0.6rem 0.8rem;margin-bottom:0.5rem;">
            <div style="color:#5a7a99;font-size:0.6rem;letter-spacing:2px;text-transform:uppercase;">Logged In</div>
            <div style="color:#00ffe7;font-family:'Orbitron',monospace;font-size:0.85rem;margin-top:0.2rem;">
                {st.session_state.username.upper()}
            </div>
        </div>
        """, unsafe_allow_html=True)
        if st.button("🚪  Logout", key="logout_btn"):
            st.session_state.logged_in = False
            st.session_state.token     = ""
            st.session_state.username  = ""
            st.session_state.page      = "Home"
            st.rerun()
    else:
        if st.button("🔑  Login / Register", key="login_btn"):
            st.session_state.page = "Login"

    st.markdown("<hr style='margin:0.5rem 0;'>", unsafe_allow_html=True)

    nav_items = [
        ("⚡", "Home",      "Overview"),
        ("👤", "Profile",   "Setup & Metrics"),
        ("🏋️", "Workout",   "AI Training Plan"),
        ("🥗", "Diet",      "Nutrition Engine"),
        ("🔥", "Calories",  "Burned Predictor"),
        ("⚠️", "Injury",   "Risk Analysis"),
        ("📊", "Score",     "Fitness Score"),
        ("📈", "Dashboard", "Live Analytics"),
        ("🤖", "Chatbot",   "AI Coach"),
        ("🎥", "CV",        "Rep Counter"),
        ("📋", "History",   "Workout Log"),
        ("📄", "Report",    "Export PDF"),
    ]
    for icon, page_name, desc in nav_items:
        if st.button(f"{icon}  {page_name}   —   {desc}", key=page_name):
            st.session_state.page = page_name

    # Dataset + backend status
    st.markdown("<hr style='margin:0.8rem 0 0.5rem;'>", unsafe_allow_html=True)
    import os
    data_dir = os.path.join(os.path.dirname(__file__), "data")
    st.markdown("""<div style="color:#5a7a99;font-size:0.65rem;letter-spacing:2px;
    text-transform:uppercase;margin-bottom:0.4rem;">Status</div>""", unsafe_allow_html=True)

    items = [
        ("bodyPerformance.csv", "Workout ML"),
        ("calories.csv",        "Calories ML"),
        ("nutrition.csv",       "Nutrition DB"),
    ]
    for fname, label in items:
        exists = os.path.exists(os.path.join(data_dir, fname))
        st.markdown(f"""<div style="color:{'#00ffe7' if exists else '#5a7a99'};
        font-size:0.72rem;margin-bottom:0.2rem;">{'🟢' if exists else '🔴'} {label}</div>""",
        unsafe_allow_html=True)

    # Backend status
    try:
        from api_client import check_backend
        be_ok = check_backend()
    except Exception:
        be_ok = False
    st.markdown(f"""<div style="color:{'#00ffe7' if be_ok else '#5a7a99'};
    font-size:0.72rem;margin-top:0.2rem;">{'🟢' if be_ok else '🔴'} Backend API</div>""",
    unsafe_allow_html=True)

# ── Page routing ───────────────────────────────────────────────────────────────
page = st.session_state.page

if   page == "Home":      from pages.home        import show
elif page == "Login":     from pages.login       import show
elif page == "Profile":   from pages.profile     import show
elif page == "Workout":   from pages.workout     import show
elif page == "Diet":      from pages.diet        import show
elif page == "Calories":  from pages.calories    import show
elif page == "Injury":    from pages.injury      import show
elif page == "Score":     from pages.score       import show
elif page == "Dashboard": from pages.dashboard   import show
elif page == "Chatbot":   from pages.chatbot     import show
elif page == "CV":        from pages.cv_exercise import show
elif page == "History":   from pages.history     import show
elif page == "Report":    from pages.report      import show

show()
