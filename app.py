import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Setup Secure Clients
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Founder, check your Secrets Dashboard!")
    st.stop()

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. Session State Logic
if "user" not in st.session_state:
    st.session_state.user = None

# --- NEW: MANUAL RECOVERY SECTION ---
def attempt_manual_login(token):
    try:
        res = supabase.auth.set_session(token, "")
        st.session_state.user = res.user
        st.success("Neural Link Established!")
        st.rerun()
    except Exception as e:
        st.error(f"Invalid Token: {e}")

# 4. Premium Dark UI (CSS)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #080a0c 100%); color: #E0E0E0; }
    .auth-card {
        background: rgba(255, 255, 255, 0.03); backdrop-filter: blur(15px);
        padding: 40px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; margin-top: 20px;
    }
    .stButton>button { 
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background: linear-gradient(90deg, #7D2AE8, #A066FF); color: white; border: none;
    }
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #7D2AE8; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 5. Login Interface
if st.session_state.user is None:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/100/shield.png", width=70)
    st.markdown("<h1>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Founder Neural Link Initialization</p><br>", unsafe_allow_html=True)
    
    # --- MAGIC LINK SECTION ---
    email_input = st.text_input("Enter Email for Magic Link", placeholder="founder@mythical.online")
    if st.button("🚀 SEND MAGIC ACCESS LINK"):
        if email_input:
            try:
                supabase.auth.sign_in_with_otp({"email": email_input})
                st.info("Access link sent! If the link just opens this page again, copy the 'access_token' from the URL and paste it below.")
            except Exception as e:
                st.error(f"Error: {e}")
    
    st.markdown("<p style='color: #444; margin: 15px 0;'>— OR —</p>", unsafe_allow_html=True)

    # --- MANUAL TOKEN RECOVERY (The Loop Breaker) ---
    token_input = st.text_input("Manual Access Token", placeholder="Paste access_token from URL here...")
    if st.button("🔓 OVERRIDE & ENTER"):
        if token_input:
            attempt_manual_login(token_input)

    st.markdown("<p style='color: #444; margin: 20px 0;'>— OR —</p>", unsafe_allow_html=True)

    # Password Fallback
    e = st.text_input("Login with Password", key="l_email")
    p = st.text_input("Password", type="password", key="l_pass")
    if st.button("INITIALIZE WITH PASSWORD"):
        try:
            res = supabase.auth.sign_in_with_password({"email": e, "password": p})
            st.session_state.user = res.user
            st.rerun()
        except:
            st.error("Invalid Credentials.")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Main Terminal (Logged In)
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #7D2AE8; text-align: center;'>MYTHICAL</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'><b>FOUNDER</b><br><small>{st.session_state.user.email}</small></div>", unsafe_allow_html=True)
        st.markdown("---")
        if st.button("🔴 LOGOUT"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    st.markdown("### 🦾 Neural Terminal")
    if "messages" not in st.session_state: st.session_state.messages = []
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]): st.markdown(msg["content"])

    if prompt := st.chat_input("Input command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)
        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Mythical AI. Concise. Professional. Owner: U. Chethan."}] + st.session_state.messages,
                    temperature=0.3
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as err: st.error(f"Error: {err}")
