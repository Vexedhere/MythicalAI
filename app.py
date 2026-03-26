import streamlit as st
from groq import Groq

# 1. Setup Client (Ensure no spaces are inside the quotes!)
client = Groq(api_key="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")

st.set_page_config(page_title="Mythical AI", page_icon="🤖")
st.title("Mythical AI 🛡️")

# 2. Simple Knowledge Base
system_message = {
    "role": "system",
    "content": "You are Mythical AI, the official assistant for Mythical Network, owned by U. Chethan. The server launches April 20, 2026. Be helpful and hyped!"
}

if "messages" not in st.session_state:
    st.session_state.messages = []

# Display chat history
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 3. Chat Logic
if prompt := st.chat_input("Ask about Mythical Network..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        try:
            # Preparing the full message list for Groq
            full_messages = [system_message] + st.session_state.messages
            
            response = client.chat.completions.create(
                model="llama3-8b-8192",
                messages=full_messages,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Founder, we have a small glitch: {e}")
