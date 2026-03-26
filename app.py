import streamlit as st
from groq import Groq

# 1. Initialize the Groq Client with your key
client = Groq(api_key="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")

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI | Official Assistant", page_icon="🤖")

st.title("Mythical AI 🛡️")
st.caption("Powered by Groq | Official Assistant for Mythical Studios")

# 3. Knowledge Base (This makes the AI smart about YOUR server)
SERVER_INFO = """
You are Mythical AI, the official assistant for Mythical Network.
- Owner: U. Chethan
- Launch Date: April 20, 2026
- Server Type: Minecraft (Survival, Skyblock, and Bedwars)
- Brand: Mythical Studios
- Goal: To provide the best lag-free gaming experience in India.
- Store: Ranks like VIP and MVP are available for purchase.
"""

# 4. Chat History Logic
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display old messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. The Chat Input
if prompt := st.chat_input("Ask about Mythical Network..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        response = client.chat.completions.create(
            model="llama3-8b-8192",
            messages=[
                {"role": "system", "content": SERVER_INFO},
                *st.session_state.messages
            ],
            temperature=0.7 # Makes the AI sound more "human" and hyped
        )
        
        answer = response.choices[0].message.content
        st.markdown(answer)
        
        # Add assistant response to history
        st.session_state.messages.append({"role": "assistant", "content": answer})

# 6. Footer
st.markdown("---")
st.caption("© 2026 Mythical Studios | Built by U. Chethan")
