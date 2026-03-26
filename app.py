import streamlit as st
from groq import Groq

# 1. Setup the Groq Client
client = Groq(api_key="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")

# 2. Page Configuration (Mobile Responsive)
st.set_page_config(page_title="Mythical AI", page_icon="🛡️", layout="centered")

# 3. Custom CSS for "PS5-Level" UI
st.markdown("""
    <style>
    /* Main Background */
    .stApp {
        background-color: #0E1117;
        color: #FFFFFF;
    }
    
    /* Chat Message Bubbles */
    .stChatMessage {
        border-radius: 15px;
        padding: 10px;
        margin-bottom: 10px;
        border: 1px solid #262730;
    }
    
    /* Sidebar Styling */
    section[data-testid="stSidebar"] {
        background-color: #161B22 !important;
        border-right: 2px solid #7D2AE8;
    }
    
    /* Input Box Styling */
    .stChatInputContainer {
        padding-bottom: 20px;
    }
    
    /* Buttons */
    .stButton>button {
        width: 100%;
        border-radius: 10px;
        background-color: #7D2AE8;
        color: white;
        border: none;
        transition: 0.3s;
    }
    .stButton>button:hover {
        background-color: #A066FF;
        transform: scale(1.02);
    }
    
    /* Hide Streamlit Header/Footer for clean look */
    header {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
    """, unsafe_allow_html=True)

# 4. Sidebar Content
with st.sidebar:
    st.markdown("<h1 style='text-align: center; color: #7D2AE8;'>MYTHICAL</h1>", unsafe_allow_html=True)
    st.image("https://via.placeholder.com/150", use_container_width=True)
    st.markdown("---")
    st.info("🚀 Launch: April 20, 2026")
    st.success("🟢 AI System Online")
    if st.button("🗑️ Clear Terminal"):
        st.session_state.messages = []
        st.rerun()

# 5. Main AI Interface
st.markdown("<h2 style='text-align: center;'>Mythical AI Assistant</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center; color: #888;'>U. Chethan's Official AI Portal</p>", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display Messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 6. Chat Logic
if prompt := st.chat_input("Message Mythical AI..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[{"role": "system", "content": "You are Mythical AI, a high-tech assistant for Mythical Network. Owner is U. Chethan. Server launches April 20, 2026. Keep it cool and hyped."}] + st.session_state.messages,
                temperature=0.7
            )
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
        except Exception as e:
            st.error(f"Founder, system glitch: {e}")
