import streamlit as st
from groq import Groq

# 1. Setup Client
client = Groq(api_key="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")

# 2. Page Config
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. Premium UI CSS
st.markdown("""
    <style>
    .stApp { background-color: #0B0E11; color: #FFFFFF; }
    .stChatMessage { border-radius: 12px; border: 1px solid #1C2128; background: #161B22; }
    section[data-testid="stSidebar"] { background-color: #0D1117 !important; border-right: 1px solid #7D2AE8; }
    .stButton>button { border-radius: 8px; background: linear-gradient(90deg, #7D2AE8, #A066FF); color: white; border: none; font-weight: bold; }
    .tier-box { padding: 10px; border-radius: 8px; margin-bottom: 10px; border: 1px solid #30363D; text-align: center; }
    header {visibility: hidden;} footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar: Tier System
with st.sidebar:
    st.markdown("<h2 style='color: #7D2AE8; text-align: center;'>MYTHICAL</h2>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/100", use_container_width=True)
    st.markdown("---")
    
    # Tier Display
    st.markdown("<div class='tier-box' style='background: rgba(125, 42, 232, 0.1); border-color: #7D2AE8;'><b>👑 FOUNDER</b><br><small>U. Chethan</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='tier-box'><b>💎 MYTHICAL PRO</b><br><small>Coming April 20</small></div>", unsafe_allow_html=True)
    st.markdown("<div class='tier-box'><b>⚡ MYTHICAL PLUS</b><br><small>Early Access</small></div>", unsafe_allow_html=True)
    
    st.markdown("---")
    if st.button("🗑️ Reset Chat"):
        st.session_state.messages = []
        st.rerun()

# 5. Main Interface
st.markdown("<h3 style='text-align: center;'>Mythical AI Portal</h3>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Ultra-Concise Logic
if prompt := st.chat_input("Ask Mythical..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "system", 
                    "content": "You are Mythical AI by Mythical Studios. Owner: U. Chethan. Rules: 1. Be ultra-concise (1 sentence max for greetings). 2. No Minecraft. 3. Professional tone."
                }] + st.session_state.messages,
                temperature=0.4
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Error: {e}")
