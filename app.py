import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Setup Secure Clients
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Founder, check your Streamlit Secrets! Keys are missing.")

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# --- NEW: SESSION RECOVERY BLOCK ---
# This catches the login if you just came back from Google
if "user" not in st.session_state:
    try:
        # Check if Supabase already has a logged-in session
        session = supabase.auth.get_session()
        if session:
            st.session_state.user = session.user
        else:
            st.session_state.user = None
    except:
        st.session_state.user = None

# 3. Premium Glassmorphism UI
st.markdown("""
    <style>
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #080a0c 100%); color: #E0E0E0; }
    .auth-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 40px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; margin-top: 30px;
    }
    .stTextInput>div>div>input { background-color: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 12px !important; }
    .stButton>button { width: 100%; border-radius: 12px; background: linear-gradient(90deg, #7D2AE8, #A066FF); color: white; border: none; font-weight: bold; height: 50px; }
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #7D2AE8; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Login Interface
if st.session_state.user is None:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/100/shield.png", width=70)
    st.markdown("<h1>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Founder Neural Link</p><br>", unsafe_allow_html=True)
    
    # --- GOOGLE LOGIN ---
    if st.button("🚀 Continue with Google"):
        try:
            res = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": { "redirect_to": "https://mythicalai.streamlit.app" }
            })
            st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"OAuth Error: {e}")

    st.markdown("<p style='color: #444; margin: 20px 0;'>— OR —</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
    with tab1:
        e = st.text_input("Email", key="l_email")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("INITIALIZE"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
            except: st.error("Access Denied.")
    with tab2:
        ne = st.text_input("New Email", key="r_email")
        np = st.text_input("New Password", type="password", key="r_pass")
        if st.button("CREATE ACCOUNT"):
            try:
                supabase.auth.sign_up({"email": ne, "password": np})
                st.success("Check your email for the link!")
            except Exception as ex: st.error(str(ex))
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Main Terminal (Logged In)
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
                    messages=[{"role": "system", "content": "You are Mythical AI. Concise. Professional."}] + st.session_state.messages,
                    temperature=0.3
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as err: st.error(f"Neural Error: {err}")
