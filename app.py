```
import os
import requests
import streamlit as st

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded",
)

# API connection
API_URL = st.secrets.get(
    "BANKING_API_URL",
    os.getenv(
        "BANKING_API_URL",
        "https://kelkoo-maybe-banana-bundle.trycloudflare.com"
    )
).rstrip("/")


# ---------------- CUSTOM DESIGN ----------------

st.markdown("""
<style>
.stApp {
    background: #F3F2EE;
    color: #26332F;
}

[data-testid="stSidebar"] {
    background: #26332F;
}

[data-testid="stSidebar"] * {
    color: #F5F0E8;
}

h1, h2, h3 {
    color: #762F48;
}

.stButton > button {
    background: #762F48;
    color: white;
    border: 0;
    border-radius: 10px;
    padding: 0.55rem 1rem;
    transition: 0.2s;
}

.stButton > button:hover {
    background: #5F2539;
    color: white;
}

div[data-testid="stChatMessage"] {
    border-radius: 12px;
}

.hero {
    background: #762F48;
    color: #F5F0E8;
    padding: 1.5rem;
    border-radius: 16px;
    margin-bottom: 1rem;
}

.hero h2 {
    color: #F5F0E8;
    margin: 0 0 .4rem 0;
}

.small-note {
    color: #65716B;
    font-size: .88rem;
}
</style>
""", unsafe_allow_html=True)


# ---------------- SIDEBAR ----------------

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


# ---------------- MAIN HEADER ----------------

st.title("Banking made simpler.")

st.markdown("""
<div class="hero">
    <h2>How can I help you today?</h2>
    <p>Ask questions about accounts, loans, cards, payments and more.</p>
</div>
""", unsafe_allow_html=True)


# ---------------- API STATUS ----------------

if not API_URL:
    st.warning("Banking AI API is not configured.")
else:
    try:
        health = requests.get(
            f"{API_URL}/health",
            timeout=10
        )

        if health.status_code == 200:
            st.success("BankMate AI is connected and ready!")
        else:
            st.warning("Banking AI backend is responding unexpectedly.")

    except requests.RequestException:
        st.warning(
            "Cannot connect to the AI backend. "
            "Please ensure the Colab server and Cloudflare tunnel are running."
        )


# ---------------- BANKING SERVICES ----------------

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


# ---------------- CHAT SECTION ----------------

st.markdown("### Chat with BankMate")

if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


question = st.chat_input("Ask your banking question...")

if st.session_state.get("pending_question"):
    question = st.session_state.pop("pending_question")


# ---------------- CHAT RESPONSE ----------------

if question:

    st.session_state.messages.append({
        "role": "user",
        "content": question
    })

    with st.chat_message("user"):
        st.markdown(question)

    with st.chat_message("assistant"):

        if not API_URL:
            answer = "The AI backend is not configured."
            st.warning(answer)

        else:
            try:
                with st.spinner("BankMate is preparing your answer..."):

                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"message": question},
                        timeout=180
                    )

                    response.raise_for_status()

                    data = response.json()

                    # Match FastAPI response format
                    answer = data.get(
                        "response",
                        "The backend did not return an answer."
                    )

                st.markdown(answer)

            except requests.Timeout:
                answer = "The AI is taking too long to respond. Please try again."
                st.error(answer)

            except requests.RequestException as exc:
                answer = (
                    "I couldn't reach the banking AI service. "
                    "Please check the Colab backend and Cloudflare tunnel."
                )
                st.error(answer)
                st.caption(f"Connection detail: {exc}")

    st.session_state.messages.append({
        "role": "assistant",
        "content": answer
    })


# ---------------- CLEAR CHAT ----------------

if st.button("Clear chat"):
    st.session_state.messages = []
    st.session_state.pop("pending_question", None)
    st.rerun()


# ---------------- SECURITY FOOTER ----------------

st.markdown("""
<p class="small-note">
BankMate AI provides general banking information, not official financial advice.
Never share your PIN, password, CVV or OTP.
</p>
""", unsafe_allow_html=True)
```
