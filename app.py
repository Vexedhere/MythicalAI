import streamlit as st
from groq import Groq

# 1. Setup the Groq Client
client = Groq(api_key="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")

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. Custom PS5-Style CSS
st.markdown("""
    <style>
    .stApp { background-color: #0E1117; color: #FFFFFF; }
    .stChatMessage { border-radius: 15px; padding: 10px; margin-bottom: 10px; border: 1px solid #262730; }
    section[data-testid="stSidebar"] { background-color: #161B22 !important; border-right: 2px solid #7D2AE8; }
    .stButton>button { width: 100%; border-radius: 10px; background-color: #7D2AE8; color: white; border: none; }
    .stButton>button:hover { background-color: #A066FF; transform: scale(1.02); }
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Content
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #7D2AE8;'>MYTHICAL</h1>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/150", use_container_width=True)
    st.markdown("---")
    st.info("💎 Project: Mythical Studios")
    st.success("🚀 Global Launch: April 20, 2026")
    if st.button("🗑️ Reset Session"):
        st.session_state.messages = []
        st.rerun()

# 5. Main AI Interface
st.markdown("<h2 style='text-align: center;'>Mythical Intelligence Portal</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>Official Studio Assistant | Founder: U. Chethan</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic (Updated System Prompt)
if prompt := st.chat_input("Inquire about Mythical Studios..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{
                    "role": "system", 
                    "content": "You are Mythical AI, the official representative of Mythical Studios. Your founder is U. Chethan. Focus on the studio's vision of high-end digital experiences and the April 20, 2026 launch. Do not mention Minecraft unless the user explicitly asks about the server. Stay professional, sleek, and high-tech."
                }] + st.session_state.messages,
                temperature=0.6
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Founder, connection error: {e}")
