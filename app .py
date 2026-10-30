import os
import requests
import streamlit as st

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="centered",
)

API_URL = st.secrets.get("BANKING_API_URL", os.getenv("BANKING_API_URL", "")).rstrip("/")

# BankMate AI – clean, minimal interface
st.markdown("""
<style>
    .stApp {
        background: #F4F3EF;
        color: #26332F;
    }
    [data-testid="stHeader"] {
        background: transparent;
    }
    [data-testid="stSidebar"] {
        background: #26332F;
    }
    [data-testid="stSidebar"] * {
        color: #F4F0E9;
    }
    .brand {
        color: #762F48;
        font-size: 1.8rem;
        font-weight: 750;
        letter-spacing: -0.5px;
        margin-bottom: 0;
    }
    .subtitle {
        color: #68736D;
        margin-top: 0.15rem;
        margin-bottom: 1.2rem;
        font-size: 0.98rem;
    }
    .topline {
        height: 5px;
        background: #762F48;
        border-radius: 20px;
        margin: 0.2rem 0 1.3rem 0;
    }
    .notice {
        background: #E8EAE3;
        border-left: 4px solid #762F48;
        padding: 0.75rem 0.9rem;
        border-radius: 8px;
        color: #3E4A44;
        font-size: 0.9rem;
        margin-bottom: 1rem;
    }
    [data-testid="stChatMessage"] {
        border-radius: 12px;
        border: 1px solid #E6E3DC;
        background: #FBFAF7;
    }
    [data-testid="stChatInput"] {
        border-color: #D9D8D1;
    }
    .stButton > button {
        background: #762F48;
        color: white;
        border: none;
        border-radius: 9px;
    }
    .stButton > button:hover {
        background: #5F2539;
        color: white;
    }
    .footer {
        color: #758078;
        font-size: 0.78rem;
        text-align: center;
        margin-top: 1rem;
    }
</style>
""", unsafe_allow_html=True)

# Small header – no extra service cards or large sidebar menu
st.markdown('<p class="brand">✦ BANKMATE AI</p>', unsafe_allow_html=True)
st.markdown(
    '<p class="subtitle">Your simple assistant for everyday banking questions</p>',
    unsafe_allow_html=True,
)
st.markdown('<div class="topline"></div>', unsafe_allow_html=True)

if not API_URL:
    st.warning("AI service is not connected. Add BANKING_API_URL in Streamlit app settings → Secrets.")
else:
    st.caption("Ask about cards, payments, savings, loans or EMI.")

# Keep chat history for the current browser session
if "messages" not in st.session_state:
    st.session_state.messages = []

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

question = st.chat_input("Ask BankMate a banking question...")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not API_URL:
            answer = "The AI service is not connected yet. Please configure BANKING_API_URL."
            st.warning(answer)
        else:
            try:
                with st.spinner("Thinking..."):
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": question},
                        timeout=180,
                    )
                    response.raise_for_status()
                    payload = response.json()
                    answer = payload.get("answer", "Sorry, I couldn't prepare an answer.")
                st.markdown(answer)
            except requests.RequestException:
                answer = (
                    "I can't reach the banking assistant right now. "
                    "Please try again in a moment."
                )
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

left, right = st.columns([1, 5])
with left:
    if st.button("Clear chat"):
        st.session_state.messages = []
        st.rerun()

st.markdown(
    '<div class="footer">BankMate AI gives general banking information only. '
    'Never share your PIN, password, CVV, OTP or full card number.</div>',
    unsafe_allow_html=True,
)
