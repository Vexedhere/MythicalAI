import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Setup Clients
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Founder, check your Secrets! Missing Keys.")

# 2. Page Config
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. Glassmorphism CSS (Updated for Google Button)
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #080a0c 100%); color: #E0E0E0; }
    .auth-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 50px;
    }
    .stButton>button { width: 100%; border-radius: 12px; font-weight: 600; height: 48px; }
    /* Google Button Custom Style */
    div[data-testid="stVerticalBlock"] > div:nth-child(3) button {
        background-color: #FFFFFF !important;
        color: #000000 !important;
        border: 1px solid #ddd !important;
    }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Session Logic
if "user" not in st.session_state:
    st.session_state.user = None

# 5. The Login UI
if st.session_state.user is None:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/100/shield.png", width=80)
    st.markdown("<h1>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Neural Link Initialization</p>", unsafe_allow_html=True)
    
    # --- ACTUAL GOOGLE LOGIN COMMAND ---
    if st.button("Continue with Google"):
        try:
            # This triggers the Supabase Google OAuth flow
            res = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": {
                    "redirect_to": "https://mythicalai.streamlit.app" # CHANGE THIS to your real Streamlit URL
                }
            })
            # Note: This will redirect the user away from the app to Google
            st.info("Redirecting to Google Secure Login...")
            st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"OAuth Error: {e}")

    st.markdown("<p style='color: #555; margin: 15px 0;'>— OR —</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Register"])
    with tab1:
        e = st.text_input("Email", key="l_email")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("Initialize"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Invalid credentials.")

    with tab2:
        ne = st.text_input("New Email", key="r_email")
        np = st.text_input("New Password", type="password", key="r_pass")
        if st.button("Create Account"):
            try:
                supabase.auth.sign_up({"email": ne, "password": np})
                st.success("Verification link sent.")
            except Exception as ex: st.error(str(ex))
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Main Interface
else:
    # (Rest of your AI code from before goes here...)
    with st.sidebar:
        st.markdown("<h2 style='color: #7D2AE8;'>MYTHICAL</h2>", unsafe_allow_html=True)
        st.write(f"Founder: {st.session_state.user.email}")
        if st.button("Logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()
    st.chat_input("Speak to Mythical...")
