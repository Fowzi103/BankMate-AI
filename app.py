import streamlit as st
import requests
import os

# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded"
)

# =====================================================
# CUSTOM CSS - PREMIUM FINTECH DESIGN
# =====================================================

st.markdown("""
<style>

/* Main application */
.stApp {
    background-color: #F5F7FB;
    color: #172033;
}

/* Main content width */
.block-container {
    max-width: 950px;
    padding-top: 2rem;
    padding-bottom: 3rem;
}

/* Main heading */
.main-title {
    font-size: 38px;
    font-weight: 800;
    color: #142B52;
    text-align: center;
    margin-bottom: 5px;
}

.main-subtitle {
    text-align: center;
    color: #64748B;
    font-size: 16px;
    margin-bottom: 25px;
}

/* Header card */
.header-card {
    background: linear-gradient(135deg, #142B52, #2455A4);
    padding: 28px;
    border-radius: 18px;
    color: white;
    text-align: center;
    margin-bottom: 25px;
    box-shadow: 0 8px 25px rgba(20, 43, 82, 0.15);
}

.header-card h2 {
    color: white;
    font-size: 27px;
    margin-bottom: 8px;
}

.header-card p {
    color: #E2EAF8;
    font-size: 14px;
    margin-bottom: 0;
}

/* Chat messages */
[data-testid="stChatMessage"] {
    background-color: white;
    border: 1px solid #E5EAF2;
    border-radius: 15px;
    padding: 15px;
    margin-bottom: 12px;
    box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
}

/* Chat input */
[data-testid="stChatInput"] {
    background-color: white;
    border-radius: 14px;
}

/* Buttons */
.stButton > button {
    background-color: #173A70;
    color: white;
    border: none;
    border-radius: 10px;
    padding: 10px 18px;
    font-weight: 600;
    transition: 0.2s ease;
}

.stButton > button:hover {
    background-color: #2455A4;
    color: white;
    border: none;
}

/* Sidebar */
[data-testid="stSidebar"] {
    background-color: #142B52;
}

[data-testid="stSidebar"] * {
    color: white;
}

[data-testid="stSidebar"] .stButton > button {
    background-color: #FFFFFF;
    color: #142B52;
    border-radius: 10px;
    font-weight: 700;
}

[data-testid="stSidebar"] .stButton > button:hover {
    background-color: #E5EDFA;
    color: #142B52;
}

/* Divider */
hr {
    border-color: #E2E8F0;
}

/* Footer */
.footer {
    text-align: center;
    color: #94A3B8;
    font-size: 12px;
    margin-top: 35px;
    padding: 15px;
}

/* Mobile responsive */
@media (max-width: 600px) {
    .main-title {
        font-size: 29px;
    }

    .header-card {
        padding: 20px;
    }

    .block-container {
        padding-left: 1rem;
        padding-right: 1rem;
    }
}

</style>
""", unsafe_allow_html=True)


# =====================================================
# BACKEND URL
# =====================================================

try:
    API_URL = st.secrets["BANKMATE_API_URL"]
except Exception:
    API_URL = os.getenv("BANKMATE_API_URL", "")

API_URL = API_URL.rstrip("/")


# =====================================================
# HEADER
# =====================================================

st.markdown("""
<div class="header-card">
    <h2>🏦 BankMate AI</h2>
    <p>Your Intelligent Banking Assistant</p>
    <p>Ask questions about banking, savings, UPI, cards and more.</p>
</div>
""", unsafe_allow_html=True)


# =====================================================
# CHAT HISTORY
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []


# Welcome message when chat is empty
if not st.session_state.messages:

    st.markdown(
        "<h3 style='text-align:center;color:#142B52;'>"
        "Welcome to BankMate AI! 👋"
        "</h3>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#64748B;'>"
        "How can I help you with your banking questions today?"
        "</p>",
        unsafe_allow_html=True
    )

    st.markdown("### 💡 Try asking")

    col1, col2 = st.columns(2)

    with col1:
        st.info("💰 What is a savings account?")
        st.info("📱 How does UPI work?")

    with col2:
        st.info("💳 What should I do if my ATM card is lost?")
        st.info("🏦 What is a fixed deposit?")


# =====================================================
# DISPLAY PREVIOUS MESSAGES
# =====================================================

for message in st.session_state.messages:

    avatar = "👤" if message["role"] == "user" else "🏦"

    with st.chat_message(message["role"], avatar=avatar):
        st.markdown(message["content"])


# =====================================================
# USER INPUT
# =====================================================

prompt = st.chat_input("💬 Ask BankMate AI anything...")


if prompt:

    # Save user message
    st.session_state.messages.append({
        "role": "user",
        "content": prompt
    })

    # Display user message
    with st.chat_message("user", avatar="👤"):
        st.markdown(prompt)

    # Generate assistant response
    with st.chat_message("assistant", avatar="🏦"):

        if not API_URL:

            st.error(
                "Backend URL is not configured. "
                "Please add BANKMATE_API_URL in Streamlit Secrets."
            )

        else:

            with st.spinner("🏦 BankMate AI is thinking..."):

                try:

                    response = requests.post(
                        f"{API_URL}/chat",
                        json={"message": prompt},
                        timeout=180
                    )

                    response.raise_for_status()

                    data = response.json()
                    answer = data.get("response")

                    if not answer:

                        st.error(
                            "The backend returned an empty answer. "
                            "Please try again."
                        )

                    else:

                        st.markdown(answer)

                        st.session_state.messages.append({
                            "role": "assistant",
                            "content": answer
                        })

                except requests.exceptions.Timeout:

                    st.error(
                        "The AI server took too long to respond. "
                        "Please try again."
                    )

                except requests.exceptions.ConnectionError:

                    st.error(
                        "Could not connect to the AI server. "
                        "Please check whether your Colab backend "
                        "and Cloudflare tunnel are running."
                    )

                except requests.exceptions.RequestException as e:

                    st.error(f"Backend error: {e}")

                except ValueError:

                    st.error(
                        "The backend returned an invalid response."
                    )


# =====================================================
# SIDEBAR
# =====================================================

with st.sidebar:

    st.markdown(
        "<h2 style='text-align:center;'>🏦 BankMate AI</h2>",
        unsafe_allow_html=True
    )

    st.markdown(
        "<p style='text-align:center;color:#DCE7F7;'>"
        "Your personal AI-powered banking assistant."
        "</p>",
        unsafe_allow_html=True
    )

    st.divider()

    st.markdown("### 💬 Chat Options")

    if st.button("🗑️ Clear Chat", use_container_width=True):

        st.session_state.messages = []
        st.rerun()

    st.divider()

    st.markdown("### 🤖 AI Information")

    st.markdown("**Model:** Qwen3-4B + LoRA")

    st.markdown("**Backend:** FastAPI")

    st.markdown("**Frontend:** Streamlit")

    st.divider()

    st.caption("🔒 BankMate AI – Your intelligent banking companion")


# =====================================================
# FOOTER
# =====================================================

st.markdown("""
<div class="footer">
    BankMate AI | Powered by Qwen3-4B + LoRA
    <br>
    AI-powered banking assistance
</div>
""", unsafe_allow_html=True)
