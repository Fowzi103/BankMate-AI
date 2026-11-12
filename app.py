
import streamlit as st
import requests
import os

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦"
)

API_URL = st.secrets.get(
    "BANKMATE_API_URL",
    os.getenv("BANKMATE_API_URL", "")
)

st.title("🏦 BankMate AI")
st.caption("Your Intelligent Banking Assistant")

if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

prompt = st.chat_input("Ask BankMate AI anything...")

if prompt:
    st.session_state.messages.append(
        {"role": "user", "content": prompt}
    )

    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        if not API_URL:
            st.error("Backend URL is not configured.")
        else:
            with st.spinner("BankMate AI is thinking..."):
                try:
                    response = requests.post(
                        f"{API_URL.rstrip('/')}/chat",
                        json={"message": prompt},
                        timeout=180
                    )
                    response.raise_for_status()

                    answer = response.json()["response"]
                    st.markdown(answer)

                    st.session_state.messages.append(
                        {"role": "assistant", "content": answer}
                    )

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend connection error: {e}")

with st.sidebar:
    st.title("🏦 BankMate AI")
    st.write("Your AI-powered banking assistant.")

    if st.button("Clear Chat"):
        st.session_state.messages = []
        st.rerun()
