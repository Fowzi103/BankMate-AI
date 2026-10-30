import os
import requests
import streamlit as st

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

API_URL = st.secrets.get("BANKING_API_URL", os.getenv("BANKING_API_URL", "")).rstrip("/")

st.markdown("""
<style>
.stApp { background: #F3F2EE; color: #26332F; }
[data-testid="stSidebar"] { background: #26332F; }
[data-testid="stSidebar"] * { color: #F5F0E8; }
h1, h2, h3 { color: #762F48; }
.stButton > button {
    background: #762F48; color: white; border: 0;
    border-radius: 10px; padding: 0.55rem 1rem;
}
.stButton > button:hover { background: #5F2539; color: white; }
div[data-testid="stChatMessage"] { border-radius: 12px; }
.hero {
    background: #762F48; color: #F5F0E8; padding: 1.5rem;
    border-radius: 16px; margin-bottom: 1rem;
}
.hero h2 { color: #F5F0E8; margin: 0 0 .4rem 0; }
.small-note { color: #65716B; font-size: .88rem; }
</style>
""", unsafe_allow_html=True)

with st.sidebar:
    st.markdown("## ✦ BANKMATE AI")
    st.caption("Your Smart Banking Assistant")
    st.divider()
    st.markdown("### Banking services")
    st.markdown("💳 Cards & payments")
    st.markdown("🏦 Loans")
    st.markdown("💰 Savings")
    st.markdown("📊 EMI & interest")
    st.divider()
    st.caption("Powered by fine-tuned Qwen3-4B")

st.title("Banking made simpler.")
st.markdown("""
<div class="hero">
  <h2>How can I help you today?</h2>
  <p>Ask questions about accounts, loans, cards, payments and more.</p>
</div>
""", unsafe_allow_html=True)

if not API_URL:
    st.warning(
        "The banking model API is not connected yet. "
        "Add BANKING_API_URL in Streamlit Cloud → App settings → Secrets."
    )

st.markdown("### Explore banking services")
suggestions = {
    "💳 Cards": "How can I block my debit card if it is lost?",
    "🏦 Loans": "What are the personal loan eligibility requirements?",
    "💰 Savings": "What is a savings account?",
    "📊 EMI": "Explain how EMI works.",
}
cols = st.columns(4)
for col, (label, prompt) in zip(cols, suggestions.items()):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state["pending_question"] = prompt

st.markdown("### Chat with BankMate")
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

question = st.chat_input("Ask your banking question...")
if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):
        if not API_URL:
            answer = "The AI backend is not connected. Please configure BANKING_API_URL."
            st.warning(answer)
        else:
            try:
                with st.spinner("BankMate is preparing your answer..."):
                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"question": question},
                        timeout=180,
                    )
                    response.raise_for_status()
                    data = response.json()
                    answer = data.get("answer", "The backend did not return an answer.")
                st.markdown(answer)
            except requests.RequestException as exc:
                answer = (
                    "I couldn't reach the banking AI service. "
                    "Please check that the Colab backend and tunnel are running."
                )
                st.error(answer)
                st.caption(f"Connection detail: {exc}")

    st.session_state.messages.append({"role": "assistant", "content": answer})

if st.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.pop("pending_question", None)
    st.rerun()

st.markdown(
    '<p class="small-note">BankMate AI provides general banking information, '
    'not official financial advice. Never share your PIN, password, CVV or OTP.</p>',
    unsafe_allow_html=True,
)
