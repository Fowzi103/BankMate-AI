
import streamlit as st
import requests
import os

# -------------------------------
# Page configuration
# -------------------------------
st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="centered"
)

# -------------------------------
# Backend URL
# -------------------------------
try:
    API_URL = st.secrets["BANKMATE_API_URL"]
except Exception:
    API_URL = os.getenv("BANKMATE_API_URL", "")

# -------------------------------
# Application heading
# -------------------------------
st.title("🏦 BankMate AI")
st.caption("Your Intelligent Banking Assistant")
st.divider()

# -------------------------------
# Chat history
# -------------------------------
if "messages" not in st.session_state:
    st.session_state.messages = []

# Display previous messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

# -------------------------------
# User input
# -------------------------------
prompt = st.chat_input("Ask BankMate AI anything...")

if prompt:

    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

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

                    data = response.json()
                    answer = data.get("response")

                    if not answer:
                        st.error("The backend returned an empty answer.")
                    else:
                        st.markdown(answer)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                except requests.exceptions.Timeout:
                    st.error("The AI server took too long to respond.")

                except requests.exceptions.ConnectionError:
                    st.error(
                        "Could not connect to the AI server. "
                        "Please check whether your Colab backend and tunnel are running."
                    )

                except requests.exceptions.RequestException as e:
                    st.error(f"Backend error: {e}")

                except ValueError:
                    st.error("The backend returned an invalid response.")

# -------------------------------
# Sidebar
# -------------------------------
with st.sidebar:

    st.title("🏦 BankMate AI")

    st.write(
        "Your personal AI-powered banking assistant."
    )

    st.divider()

    if st.button("Clear Chat", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

    st.caption("Powered by Qwen3-4B + LoRA")
