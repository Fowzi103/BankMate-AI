import os
import requests
import streamlit as st

st.set_page_config(page_title="BankMate AI", page_icon="🏦", layout="wide")

BURGUNDY = "#762F48"
SAGE = "#26332F"
GOLD = "#D7B875"
IVORY = "#F3F2EE"

st.markdown(f"""
<style>
.stApp {{ background:{IVORY}; color:{SAGE}; }}
[data-testid="stSidebar"] {{ background:{SAGE}; }}
[data-testid="stSidebar"] * {{ color:#F5F0E8; }}
h1,h2,h3 {{ color:{BURGUNDY}; }}
.stButton > button {{ background:{BURGUNDY}; color:white; border:0; border-radius:9px; }}
div[data-testid="stChatMessage"] {{ border-radius:12px; }}
.hero {{ background:{BURGUNDY}; padding:24px; border-radius:16px; color:white; }}
.hero h2 {{ color:#F5F0E8; margin:0 0 8px 0; }}
.small-note {{ color:#68736D; font-size:0.85rem; }}
</style>
""", unsafe_allow_html=True)

def get_api_url():
    try:
        return st.secrets.get("BANKING_API_URL", os.getenv("BANKING_API_URL", "")).rstrip("/")
    except Exception:
        return os.getenv("BANKING_API_URL", "").rstrip("/")

with st.sidebar:
    st.markdown("## ✦ BANKMATE AI")
    st.caption("Your Smart Banking Assistant")
    st.divider()
    st.markdown("### Banking Services")
    st.markdown("💳 Cards & Payments")
    st.markdown("🏦 Loans")
    st.markdown("💰 Savings")
    st.markdown("📊 EMI & Interest")
    st.divider()
    st.caption("Fine-tuned Qwen3-4B + LoRA")
    if st.button("Clear conversation", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("""
<div class="hero">
  <h2>Banking made simpler.</h2>
  Ask questions about accounts, cards, loans, payments and digital banking.
</div>
""", unsafe_allow_html=True)

st.subheader("Explore banking services")
suggestions = [
    ("💳 Cards & Payments", "How can I block my debit card if it is lost?"),
    ("🏦 Loans", "What documents are usually required for a personal loan?"),
    ("💰 Savings", "What is the difference between a fixed deposit and a recurring deposit?"),
    ("📊 EMI & Interest", "Explain how monthly loan EMI works."),
]
cols = st.columns(4)
for col, (label, prompt) in zip(cols, suggestions):
    with col:
        if st.button(label, use_container_width=True):
            st.session_state.pending_prompt = prompt

if "messages" not in st.session_state:
    st.session_state.messages = []
if "pending_prompt" not in st.session_state:
    st.session_state.pending_prompt = ""

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

typed_prompt = st.chat_input("Ask your banking question...")
question = st.session_state.pending_prompt or typed_prompt
st.session_state.pending_prompt = ""

if question:
    st.session_state.messages.append({"role": "user", "content": question})
    with st.chat_message("user"):
        st.markdown(question)

    api_url = get_api_url()
    with st.chat_message("assistant"):
        if not api_url:
            answer = (
                "The chat interface is ready, but the model API is not connected yet. "
                "Set `BANKING_API_URL` in Streamlit Cloud → App settings → Secrets "
                "to the URL of your GPU inference server."
            )
            st.info(answer)
        else:
            try:
                with st.spinner("BankMate is thinking..."):
                    response = requests.post(
                        f"{api_url}/chat",
                        json={"question": question},
                        timeout=180,
                    )
                    response.raise_for_status()
                    answer = response.json().get("answer", "The model returned an empty response.")
                st.markdown(answer)
            except requests.RequestException as exc:
                answer = f"Could not reach the model server. Please check that the GPU server is running. Details: {exc}"
                st.error(answer)

    st.session_state.messages.append({"role": "assistant", "content": answer})

st.caption("BankMate AI provides general banking information, not official financial advice. Never share PINs, passwords, CVVs or OTPs.")
