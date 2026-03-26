import streamlit as st
from groq import Groq

# 1. Setup the Groq Client with your key
# Founder Tip: Keep the quotes exactly like this.
client = Groq(api_key="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")

# 2. Page Configuration
st.set_page_config(page_title="Mythical AI | Official Assistant", page_icon="🤖")

st.title("Mythical AI 🛡️")
st.caption("Official Assistant for U. Chethan's Mythical Network")

# 3. The "Brain" (Knowledge Base)
# Edit this text below to add your server rules or IP address!
system_message = {
    "role": "system", 
    "content": """
    You are Mythical AI, the professional assistant for Mythical Network.
    - Owner: U. Chethan
    - Launch Date: April 20, 2026
    - Brand: Mythical Studios
    - Goal: Provide a top-tier Minecraft experience.
    Be helpful, hyped for the launch, and always loyal to U. Chethan.
    """
}

# 4. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# 5. Chat Input Logic
if prompt := st.chat_input("Ask about the April 20 launch..."):
    # Add user message to history
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    # Generate AI Response
    with st.chat_message("assistant"):
        try:
            # Using the latest 2026-ready model: llama-3.3-70b-versatile
            response = client.chat.completions.create(
                model="llama-3.3-70b-versatile",
                messages=[system_message] + st.session_state.messages,
                temperature=0.7
            )
            
            answer = response.choices[0].message.content
            st.markdown(answer)
            
            # Save assistant response to history
            st.session_state.messages.append({"role": "assistant", "content": answer})
            
        except Exception as e:
            st.error(f"Founder, we hit a snag. Error: {e}")

# 6. Sidebar Info
with st.sidebar:
    st.image("https://via.placeholder.com/150", caption="Mythical Studios")
    st.write("---")
    st.info("Status: AI Online 🟢")
    if st.button("Clear Chat History"):
        st.session_state.messages = []
        st.rerun()

# 7. Footer
st.markdown("---")
st.caption("© 2026 Mythical Studios | Built by U. Chethan")
