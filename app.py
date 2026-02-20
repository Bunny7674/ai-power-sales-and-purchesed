import streamlit as st
import requests

st.set_page_config(page_title="MarketMind AI", layout="wide")

# ---------- SIDEBAR ----------
st.sidebar.title("⚙ AI Settings")

model_choice = st.sidebar.selectbox(
    "Select Model",
    ["OpenAI", "Grok"]
)

temperature = st.sidebar.slider("Creativity (Temperature)", 0.0, 1.0, 0.3)

if st.sidebar.button("Clear Chat"):
    st.session_state.messages = []

# ---------- SESSION MEMORY ----------
if "messages" not in st.session_state:
    st.session_state.messages = []

# ---------- TITLE ----------
st.title("🧠 MarketMind AI Sales Agent")

st.markdown("Ask about sales predictions, company knowledge, marketing ideas, or generate creatives.")

# ---------- CHAT DISPLAY ----------
for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

# ---------- INPUT ----------
user_input = st.chat_input("Ask your AI Sales Agent...")

if user_input:

    st.session_state.messages.append({"role": "user", "content": user_input})

    with st.chat_message("user"):
        st.markdown(user_input)

    # Call backend
    response = requests.post(
        "http://127.0.0.1:5000/agent",
        json={
            "query": user_input,
            "model": model_choice,
            "temperature": temperature
        }
    )

    result = response.json()["response"]

    st.session_state.messages.append({"role": "assistant", "content": result})

    with st.chat_message("assistant"):
        st.markdown(result)
