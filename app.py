import streamlit as st
from groq import Groq
from supabase import create_client

# 1. Setup Clients (Securely using the keys you provided)
# Note: In a real launch, move these to Streamlit Settings > Secrets!
SB_URL = 'https://mtczyuzbcunsflvcnatf.supabase.co'
SB_KEY = 'sb_publishable_AKAJaNZknnvnHQOQVR3JSQ_Xopmf6yk'

supabase = create_client(SB_URL, SB_KEY)
client = Groq(api_key=st.secrets["GROQ_API_KEY"])

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI Portal", page_icon="🛡️", layout="centered")

# 3. Custom Studio CSS (Gamer & Tech Theme)
st.markdown("""
    <style>
    .stApp { background-color: #080A0C; color: #E0E0E0; }
    [data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 2px solid #7D2AE8; }
    
    /* Login Card */
    .auth-container {
        background: #161B22;
        padding: 40px;
        border-radius: 20px;
        border: 1px solid #30363D;
        text-align: center;
        box-shadow: 0 10px 30px rgba(0,0,0,0.5);
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 12px;
        background: linear-gradient(135deg, #7D2AE8 0%, #4B1291 100%);
        color: white;
        border: none;
        font-weight: 700;
        height: 50px;
        transition: 0.3s;
    }
    .stButton>button:hover { transform: translateY(-2px); box-shadow: 0 5px 15px rgba(125, 42, 232, 0.4); }
    
    /* Input Fields */
    .stTextInput>div>div>input {
        background-color: #0D1117;
        color: white;
        border: 1px solid #30363D;
        border-radius: 10px;
    }
    
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Auth Session State
if "user" not in st.session_state:
    st.session_state.user = None

# 5. The Login UI
if st.session_state.user is None:
    st.markdown("<div class='auth-container'>", unsafe_allow_html=True)
    # REPLACE THIS URL WITH YOUR ACTUAL LOGO
    st.image("https://img.icons8.com/isometric/100/shield.png", width=100)
    st.markdown("<h1 style='color: #7D2AE8;'>MYTHICAL STUDIOS</h1>", unsafe_allow_html=True)
    st.markdown("<p style='color: #888;'>Secure Neural Link Initialization</p>", unsafe_allow_html=True)
    
    tab1, tab2 = st.tabs(["⚡ LOGIN", "💎 REGISTER"])
    
    with tab1:
        email = st.text_input("Email Address", key="l_email")
        password = st.text_input("Password", type="password", key="l_pass")
        if st.button("INITIALIZE SESSION"):
            try:
                res = supabase.auth.sign_in_with_password({"email": email, "password": password})
                st.session_state.user = res.user
                st.rerun()
            except:
                st.error("Access Denied: Check Credentials")
                
    with tab2:
        n_email = st.text_input("Email Address", key="r_email")
        n_pass = st.text_input("Password", type="password", key="r_pass")
        if st.button("CREATE FOUNDER ACCOUNT"):
            try:
                supabase.auth.sign_up({"email": n_email, "password": n_pass})
                st.info("Verification link sent to your email!")
            except Exception as e:
                st.error(f"Error: {e}")
    st.markdown("</div>", unsafe_allow_html=True)

# 6. Main Dashboard (Logged In)
else:
    with st.sidebar:
        st.markdown("<h2 style='text-align: center; color: #7D2AE8;'>MYTHICAL AI</h2>", unsafe_allow_html=True)
        # Placeholder for Founder Image
        st.image("https://img.icons8.com/fluency/100/user-shield.png", width=100)
        st.markdown(f"<p style='text-align: center;'><b>FOUNDER</b><br>{st.session_state.user.email}</p>", unsafe_allow_html=True)
        st.markdown("---")
        st.info("⚡ System: Optimal")
        st.success("🚀 Launch: April 20")
        
        if st.button("LOGOUT"):
            supabase.auth.sign_out()
            st.session_state.user = None
            st.rerun()

    # --- Chat Interface ---
    st.markdown("### 🦾 Neural Interface")
    
    if "messages" not in st.session_state:
        st.session_state.messages = []

    for msg in st.session_state.messages:
        with st.chat_message(msg["role"]):
            st.markdown(msg["content"])

    if prompt := st.chat_input("Input command..."):
        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"): st.markdown(prompt)

        with st.chat_message("assistant"):
            try:
                response = client.chat.completions.create(
                    model="llama-3.3-70b-versatile",
                    messages=[{"role": "system", "content": "You are Mythical AI for Mythical Studios. Owner: U. Chethan. Be ultra-concise, professional, and high-tech."}] + st.session_state.messages,
                    temperature=0.4
                )
                answer = response.choices[0].message.content
                st.markdown(answer)
                st.session_state.messages.append({"role": "assistant", "content": answer})
            except Exception as e:
                st.error(f"Neural Link Error: {e}")
