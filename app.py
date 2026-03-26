import streamlit as st
from groq import Groq
from supabase import create_client
import time

# 1. Initialize Clients from Secrets
try:
    # Use the keys you provided in your Streamlit Secrets dashboard
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Founder, check your Streamlit Secrets! Missing keys.")
    st.stop()

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# --- AUTHENTICATION ENGINE ---
if "user" not in st.session_state:
    st.session_state.user = None

# This block catches the user if they just returned from Google
def sync_session():
    try:
        # Check if Supabase has a logged-in session in the browser
        res = supabase.auth.get_session()
        if res and res.session:
            st.session_state.user = res.session.user
        else:
            # Fallback: check if a user object exists
            user_res = supabase.auth.get_user()
            if user_res:
                st.session_state.user = user_res.user
    except:
        st.session_state.user = None

sync_session()

# 3. Custom Elite UI (CSS)
st.markdown("""
    <style>
    /* Dark Gradient Background */
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #080a0c 100%); color: #E0E0E0; }
    
    /* Center Card UI */
    .auth-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(15px);
        padding: 40px; border-radius: 24px; border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center; margin-top: 20px;
    }
    
    /* Modern Inputs */
    .stTextInput>div>div>input { background-color: rgba(255,255,255,0.05) !important; color: white !important; border-radius: 12px !important; }
    
    /* Mythical Purple Button */
    .stButton>button {
        width: 100%; border-radius: 12px; height: 50px; font-weight: bold;
        background: linear-gradient(90deg, #7D2AE8, #A066FF); color: white; border: none;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: scale(1.02); box-shadow: 0 0 20px rgba(125, 42, 232, 0.5); }
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #7D2AE8; }
    
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Login Interface
if st.session_state.user is None:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/100/shield.png", width=70)
    st.markdown("<h1 style='margin-bottom:0;'>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Founder Neural Link Initialization</p><br>", unsafe_allow_html=True)
    
    # --- GOOGLE OAUTH ---
    if st.button("🚀 Continue with Google"):
        try:
            # IMPORTANT: Ensure this URL matches your Streamlit URL exactly
            redirect_url = "https://mythicalai.streamlit.app" 
            res = supabase.auth.sign_in_with_oauth({
                "provider": "google",
                "options": { "redirect_to": redirect_url }
            })
            if res.url:
                st.info("Redirecting to Secure Neural Link...")
                st.markdown(f'<meta http-equiv="refresh" content="0;url={res.url}">', unsafe_allow_html=True)
        except Exception as e:
            st.error(f"OAuth Error: {e}")

    st.markdown("<p style='color: #444; margin: 20px 0;'>— OR —</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["LOGIN", "REGISTER"])
    with tab1:
        e = st.text_input("Email", key="l_email")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("INITIALIZE SESSION"):
            try:
                auth_res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = auth_res.user
                st.rerun()
            except: st.error("Access Denied: Invalid Credentials")

    with tab2:
        ne = st.text_input("New Email", key="r_email")
        np = st.text_input("New Password", type="password", key="r_pass")
        if st.button("CREATE FOUNDER ID"):
            try:
                supabase.auth.sign_up({"email": ne, "password": np})
                st.success("Verification link sent! Check your inbox.")
            except Exception as ex: st.error(str(ex))
    st.markdown("</div>", unsafe_allow_html=True)

# 5. Main Terminal (Logged In)
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #7D2AE8; text-align: center;'>MYTHICAL</h2>", unsafe_allow_html=True)
        st.markdown(f"<div style='text-align:center;'><b>FOUNDER ACCESS</b><br><small>{st.session_state.user.email}</small></div>", unsafe_allow_html=True)
        st.markdown("---")
        st.write("🏆 **PRO ACTIVATED**")
        st.write("⚡ **PLUS ENABLED**")
        st.markdown("---")
        if st.button("🔴 DEACTIVATE (Logout)"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    st.markdown("### 🦾 Neural Terminal")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    # Display Chat History
    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    # Chat Input
    if prompt := st.chat_input("Command Mythical AI..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Mythical AI by Mythical Studios. Owner: U. Chethan. Rules: 1. Max 2 sentences. 2. Professional/High-tech tone. 3. No MC mentions."}] + st.session_state.messages,
                    temperature=0.3
                )
                ans = response.choices[0].message.content
                st.markdown(ans)
                st.session_state.messages.append({"role": "assistant", "content": ans})
            except Exception as err:
                st.error(f"Neural Interface Glitch: {err}")
