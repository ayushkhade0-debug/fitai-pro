import streamlit as st
import sys, os
sys.path.insert(0, os.path.dirname(os.path.dirname(__file__)))
from api_client import register, login, check_backend
```

def show():
    st.markdown("""
    <div style="margin-bottom:2rem; text-align:center;">
        <div style="font-family:'Orbitron',monospace; font-size:2rem; font-weight:900;
                    background:linear-gradient(135deg,#00ffe7,#00b8ff);
                    -webkit-background-clip:text; -webkit-text-fill-color:transparent;
                    background-clip:text; letter-spacing:3px;">⚡ FITAI PRO</div>
        <div style="color:#5a7a99; font-size:0.8rem; letter-spacing:3px; margin-top:0.3rem;">
            SECURE LOGIN · JWT AUTHENTICATION · FASTAPI BACKEND
        </div>
    </div>
    """, unsafe_allow_html=True)

    # Backend status check
    backend_ok = check_backend()
    if backend_ok:
        st.markdown("""
        <div style="background:rgba(0,255,231,0.05); border:1px solid rgba(0,255,231,0.2);
                    border-radius:8px; padding:0.7rem 1rem; margin-bottom:1.5rem; text-align:center;">
            <span style="color:#00ffe7; font-size:0.8rem;">✅ Backend Connected — FastAPI running on port 8000</span>
        </div>
        """, unsafe_allow_html=True)
    else:
        st.markdown("""
        <div style="background:rgba(255,82,82,0.05); border:1px solid rgba(255,82,82,0.2);
                    border-radius:8px; padding:0.7rem 1rem; margin-bottom:1.5rem; text-align:center;">
            <span style="color:#ff5252; font-size:0.8rem;">
                ⚠️ Backend not detected — Start it with: <code>uvicorn main:app --reload</code>
            </span>
        </div>
        """, unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["🔑  Login", "📝  Register"])

    with tab1:
        with st.form("login_form"):
            st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
            text-transform:uppercase; margin-bottom:1rem;">Login to Your Account</div>""",
            unsafe_allow_html=True)
            email    = st.text_input("Email", placeholder="you@example.com")
            password = st.text_input("Password", type="password")
            submitted = st.form_submit_button("⚡  LOGIN")

        if submitted:
            if not email or not password:
                st.error("Please fill in all fields.")
            else:
                with st.spinner("Authenticating..."):
                    result, ok = login(email, password)
                if ok:
                    st.session_state.token    = result["access_token"]
                    st.session_state.user_id  = result["user_id"]
                    st.session_state.username = result["name"]
                    st.session_state.logged_in = True
                    st.success(f"✅ Welcome back, {result['name']}!")
                    st.rerun()
                else:
                    st.error(result.get("detail", "Login failed."))

    with tab2:
        with st.form("register_form"):
            st.markdown("""<div style="color:#5a7a99; font-size:0.7rem; letter-spacing:3px;
            text-transform:uppercase; margin-bottom:1rem;">Create New Account</div>""",
            unsafe_allow_html=True)
            name      = st.text_input("Full Name", placeholder="Ayush Khade")
            email_r   = st.text_input("Email", placeholder="you@example.com")
            password_r = st.text_input("Password", type="password", key="reg_pass")
            submitted_r = st.form_submit_button("📝  REGISTER")

        if submitted_r:
            if not name or not email_r or not password_r:
                st.error("Please fill in all fields.")
            elif len(password_r) < 6:
                st.error("Password must be at least 6 characters.")
            else:
                with st.spinner("Creating account..."):
                    result, ok = register(name, email_r, password_r)
                if ok:
                    st.success(f"✅ {result['message']} — Please login now!")
                else:
                    st.error(result.get("detail", "Registration failed."))
