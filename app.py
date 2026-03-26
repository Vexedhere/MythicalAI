import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Setup Clients (Pulling from Streamlit Secrets)
try:
    supabase = create_client(st.secrets["SUPABASE_URL"], st.secrets["SUPABASE_KEY"])
    client = Groq(api_key=st.secrets["GROQ_API_KEY"])
except Exception as e:
    st.error("Founder, check your Secrets! Missing Keys.")

# 2. Page Config
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. "Glassmorphism" Studio UI (Ultra Clean)
st.markdown("""
    <style>
    /* Global Dark Theme */
    .stApp { background: radial-gradient(circle at top, #1a1a2e 0%, #080a0c 100%); color: #E0E0E0; font-family: 'Inter', sans-serif; }
    
    /* Center the Login Card */
    .auth-card {
        background: rgba(255, 255, 255, 0.03);
        backdrop-filter: blur(10px);
        padding: 40px;
        border-radius: 24px;
        border: 1px solid rgba(255, 255, 255, 0.1);
        text-align: center;
        margin-top: 50px;
    }

    /* Professional Sidebar */
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #7D2AE8; }
    
    /* Styled Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: #7D2AE8;
        color: white;
        border: none;
        font-weight: 600;
        height: 48px;
        transition: all 0.3s ease;
    }
    .stButton>button:hover { background: #9D50FF; box-shadow: 0 0 20px rgba(125, 42, 232, 0.4); }

    /* Google Button Styling */
    .google-btn {
        background: white !important;
        color: #000 !important;
        margin-bottom: 20px;
    }

    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: rgba(255,255,255,0.05);
        color: white;
        border: 1px solid rgba(255,255,255,0.1);
        border-radius: 12px;
        padding: 12px;
    }

    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Session Logic
if "user" not in st.session_state:
    st.session_state.user = None

# 5. The "Elite" Login Screen
if st.session_state.user is None:
    st.markdown("<div class='auth-card'>", unsafe_allow_html=True)
    st.image("https://img.icons8.com/fluency/100/shield.png", width=80)
    st.markdown("<h1 style='letter-spacing: 2px; margin-bottom: 5px;'>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888; font-size: 14px;'>Authorized Access Only</p>", unsafe_allow_html=True)
    
    # Placeholder Google Login
    if st.button("Continue with Google", key="google_login"):
        st.info("Google OAuth is being initialized for the April 20 launch.")

    st.markdown("<p style='color: #555; margin: 15px 0;'>— OR —</p>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Create Account"])
    
    with tab1:
        e = st.text_input("Email", key="l_email")
        p = st.text_input("Password", type="password", key="l_pass")
        if st.button("Initialize"):
            try:
                res = supabase.auth.sign_in_with_password({"email": e, "password": p})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("Invalid neural credentials.")

    with tab2:
        ne = st.text_input("New Email", key="r_email")
        np = st.text_input("New Password", type="password", key="r_pass")
        if st.button("Register"):
            try:
                supabase.auth.sign_up({"email": ne, "password": np})
                st.success("Verification link sent.")
            except Exception as ex:
                st.error(f"Error: {ex}")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Main Dashboard
else:
    with st.sidebar:
        st.markdown("<h2 style='color: #7D2AE8;'>MYTHICAL</h2>", unsafe_allow_html=True)
        st.markdown(f"**Founder:** <br>`{st.session_state.user.email}`", unsafe_allow_html=True)
        st.markdown("---")
        st.write("🏆 **PRO** | ⚡ **PLUS**")
        if st.button("Logout"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    st.markdown("### Neural Interface")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Speak to AI..."):
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
            except Exception as err:
                st.error(f"Neural Error: {err}")
