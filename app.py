import os
import uuid
from datetime import date

import pandas as pd
import requests
import streamlit as st


# =====================================================
# PAGE CONFIGURATION
# =====================================================

st.set_page_config(
    page_title="BankMate AI",
    page_icon="🏦",
    layout="centered",
    initial_sidebar_state="expanded",
)


# =====================================================
# CUSTOM CSS - PREMIUM FINTECH DESIGN
# =====================================================

st.markdown(
    """
    <style>
    .stApp {
        background-color: #F5F7FB;
        color: #172033;
    }

    .block-container {
        max-width: 950px;
        padding-top: 2rem;
        padding-bottom: 3rem;
    }

    .header-card {
        background: linear-gradient(135deg, #142B52, #2455A4);
        padding: 28px;
        border-radius: 18px;
        color: #FFFFFF;
        text-align: center;
        margin-bottom: 25px;
        box-shadow: 0 8px 25px rgba(20, 43, 82, 0.15);
    }

    .header-card h2 {
        color: #FFFFFF !important;
        font-size: 27px;
        margin-bottom: 8px;
    }

    .header-card p {
        color: #E2EAF8 !important;
        font-size: 14px;
        margin-bottom: 0;
    }

    [data-testid="stChatMessage"] {
        background-color: #FFFFFF;
        border: 1px solid #E5EAF2;
        border-radius: 15px;
        padding: 15px;
        margin-bottom: 12px;
        box-shadow: 0 3px 10px rgba(15, 23, 42, 0.04);
    }

    [data-testid="stChatInput"] {
        background-color: #FFFFFF;
        border-radius: 14px;
    }

    .stButton > button {
        background-color: #173A70;
        color: #FFFFFF !important;
        border: none;
        border-radius: 10px;
        padding: 10px 18px;
        font-weight: 600;
        transition: 0.2s ease;
    }

    .stButton > button:hover {
        background-color: #2455A4;
        color: #FFFFFF !important;
        border: none;
    }

    /* Sidebar background and normal text */
    [data-testid="stSidebar"] {
        background-color: #142B52;
    }

    [data-testid="stSidebar"] h1,
    [data-testid="stSidebar"] h2,
    [data-testid="stSidebar"] h3,
    [data-testid="stSidebar"] p,
    [data-testid="stSidebar"] label,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] {
        color: #FFFFFF;
    }

    /* Sidebar buttons: force dark readable text on white background */
    [data-testid="stSidebar"] .stButton > button {
        background-color: #FFFFFF !important;
        color: #142B52 !important;
        border: 1px solid #DCE6F5 !important;
        border-radius: 10px !important;
        font-weight: 700 !important;
        min-height: 44px;
    }

    [data-testid="stSidebar"] .stButton > button *,
    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span,
    [data-testid="stSidebar"] .stButton > button div {
        color: #142B52 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover {
        background-color: #E5EDFA !important;
        color: #142B52 !important;
        border-color: #C7D8F0 !important;
    }

    [data-testid="stSidebar"] .stButton > button:hover * {
        color: #142B52 !important;
    }

    hr {
        border-color: #E2E8F0;
    }

    .footer {
        text-align: center;
        color: #94A3B8;
        font-size: 12px;
        margin-top: 35px;
        padding: 15px;
    }

    @media (max-width: 600px) {
        .header-card {
            padding: 20px;
        }

        .block-container {
            padding-left: 1rem;
            padding-right: 1rem;
        }
    }
    </style>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# BACKEND URL
# =====================================================

try:
    API_URL = st.secrets["BANKMATE_API_URL"]
except Exception:
    API_URL = os.getenv("BANKMATE_API_URL", "")

API_URL = API_URL.rstrip("/")


# =====================================================
# SESSION STATE INITIALIZATION
# =====================================================

if "messages" not in st.session_state:
    st.session_state.messages = []

if "expenses" not in st.session_state:
    st.session_state.expenses = []

if "app_page" not in st.session_state:
    st.session_state.app_page = "Chatbot"


# =====================================================
# SIDEBAR NAVIGATION
# =====================================================

with st.sidebar:
    st.markdown(
        "<h2 style='text-align:center; color:#FFFFFF;'>🏦 BankMate AI</h2>",
        unsafe_allow_html=True,
    )
    st.markdown(
        "<p style='text-align:center; color:#DCE7F7;'>"
        "Your personal AI-powered banking assistant."
        "</p>",
        unsafe_allow_html=True,
    )

    st.divider()
    st.markdown("### 📊 Banking Tools")

    if st.button("💬 AI Chatbot", use_container_width=True, key="nav_chatbot"):
        st.session_state.app_page = "Chatbot"
        st.rerun()

    if st.button(
        "💰 Expense Tracker",
        use_container_width=True,
        key="nav_expense_tracker",
    ):
        st.session_state.app_page = "Expense Tracker"
        st.rerun()

    st.divider()
    st.markdown("### 🤖 AI Information")
    st.markdown("**Model:** Qwen3-4B + LoRA")
    st.markdown("**Backend:** FastAPI")
    st.markdown("**Frontend:** Streamlit")

    st.divider()

    if st.button("🗑️ Clear Chat", use_container_width=True, key="clear_chat"):
        st.session_state.messages = []
        st.rerun()

    st.caption("🔒 BankMate AI – Your intelligent banking companion")


# =====================================================
# SHARED HEADER
# =====================================================

st.markdown(
    """
    <div class="header-card">
        <h2>🏦 BankMate AI</h2>
        <p>Your Intelligent Banking Assistant</p>
        <p>Ask questions about banking, savings, UPI, cards and more.</p>
    </div>
    """,
    unsafe_allow_html=True,
)


# =====================================================
# PAGE 1: AI CHATBOT
# =====================================================

if st.session_state.app_page == "Chatbot":

    if not st.session_state.messages:
        st.markdown(
            "<h3 style='text-align:center;color:#142B52;'>"
            "Welcome to BankMate AI! 👋</h3>",
            unsafe_allow_html=True,
        )
        st.markdown(
            "<p style='text-align:center;color:#64748B;'>"
            "How can I help you with your banking questions today?</p>",
            unsafe_allow_html=True,
        )

        st.markdown("### 💡 Try asking")
        col1, col2 = st.columns(2)

        with col1:
            st.info("💰 What is a savings account?")
            st.info("📱 How does UPI work?")

        with col2:
            st.info("💳 What should I do if my ATM card is lost?")
            st.info("🏦 What is a fixed deposit?")

    # Display previous messages
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🏦"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])

    prompt = st.chat_input("💬 Ask BankMate AI anything...")

    if prompt:
        st.session_state.messages.append(
            {"role": "user", "content": prompt}
        )

        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)

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
                            timeout=180,
                        )
                        response.raise_for_status()

                        data = response.json()
                        answer = data.get("response")

                        if not answer:
                            st.error("The backend returned an empty answer.")
                        else:
                            st.markdown(answer)
                            st.session_state.messages.append(
                                {"role": "assistant", "content": answer}
                            )

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
                    except requests.exceptions.RequestException as error:
                        st.error(f"Backend error: {error}")
                    except ValueError:
                        st.error("The backend returned an invalid response.")


# =====================================================
# PAGE 2: EXPENSE TRACKER
# =====================================================

elif st.session_state.app_page == "Expense Tracker":

    st.markdown(
        "<h1 style='color:#142B52;'>💰 Expense Tracker</h1>",
        unsafe_allow_html=True,
    )
    st.caption("Track your spending and understand where your money goes.")

    # -------------------------------------------------
    # FEATURE 1: ADD AND MANAGE EXPENSES
    # -------------------------------------------------

    st.subheader("➕ Add New Expense")

    with st.form("expense_form", clear_on_submit=True):
        amount = st.number_input(
            "Expense Amount (₹)",
            min_value=0.01,
            step=10.0,
            format="%.2f",
        )

        category = st.selectbox(
            "Expense Category",
            [
                "Food",
                "Shopping",
                "Transport",
                "Bills",
                "Entertainment",
                "Healthcare",
                "Education",
                "Other",
            ],
        )

        expense_date = st.date_input(
            "Expense Date",
            value=date.today(),
        )

        description = st.text_input(
            "Description",
            placeholder="Example: Grocery shopping",
        )

        submitted = st.form_submit_button(
            "Add Expense",
            use_container_width=True,
        )

        if submitted:
            new_expense = {
                "id": uuid.uuid4().hex,
                "amount": float(amount),
                "category": category,
                "date": expense_date.isoformat(),
                "description": description.strip(),
            }

            st.session_state.expenses.append(new_expense)
            st.success("Expense added successfully!")
            st.rerun()

    st.divider()

    # -------------------------------------------------
    # FEATURE 2: EXPENSE ANALYTICS
    # -------------------------------------------------

    st.subheader("📈 Expense Analytics")

    if st.session_state.expenses:
        df = pd.DataFrame(st.session_state.expenses)
        df["date"] = pd.to_datetime(df["date"], errors="coerce")
        df["amount"] = pd.to_numeric(df["amount"], errors="coerce")
        df = df.dropna(subset=["date", "amount"])

        current_month = date.today().strftime("%Y-%m")
        monthly_df = df[
            df["date"].dt.strftime("%Y-%m") == current_month
        ]

        total_spending = float(df["amount"].sum())
        monthly_spending = float(monthly_df["amount"].sum())

        col1, col2 = st.columns(2)
        col1.metric("Total Expenses", f"₹{total_spending:,.2f}")
        col2.metric("This Month", f"₹{monthly_spending:,.2f}")

        st.markdown("### Category-wise Spending")
        category_data = (
            df.groupby("category")["amount"]
            .sum()
            .sort_values(ascending=False)
        )
        st.bar_chart(category_data)

        st.markdown("### Expense History")
        display_df = df.sort_values("date", ascending=False).copy()
        display_df["date"] = display_df["date"].dt.strftime("%d-%m-%Y")
        display_df = display_df[
            ["date", "description", "category", "amount"]
        ]
        display_df.columns = [
            "Date",
            "Description",
            "Category",
            "Amount (₹)",
        ]

        st.dataframe(
            display_df,
            use_container_width=True,
            hide_index=True,
        )

        # CSV download
        csv_df = df.drop(columns=["id"]).copy()
        csv_df["date"] = csv_df["date"].dt.strftime("%Y-%m-%d")
        csv_data = csv_df.to_csv(index=False).encode("utf-8")

        st.download_button(
            "⬇️ Download Expense Report (CSV)",
            data=csv_data,
            file_name="bankmate_expenses.csv",
            mime="text/csv",
            use_container_width=True,
        )

        # Delete expense: ID is used internally so duplicate descriptions
        # or identical amounts do not cause the wrong record to be deleted.
        st.markdown("### 🗑️ Manage Expenses")

        expense_by_id = {
            item["id"]: item
            for item in st.session_state.expenses
        }

        expense_ids = list(reversed(list(expense_by_id.keys())))

        def expense_label(expense_id):
            item = expense_by_id[expense_id]
            description_text = item["description"] or "No description"
            return (
                f"{item['date']} | ₹{item['amount']:.2f} | "
                f"{item['category']} | {description_text}"
            )

        selected_id = st.selectbox(
            "Select an expense to delete",
            options=expense_ids,
            format_func=expense_label,
            key="expense_to_delete",
        )

        if st.button(
            "Delete Selected Expense",
            use_container_width=True,
            key="delete_expense",
        ):
            st.session_state.expenses = [
                item
                for item in st.session_state.expenses
                if item["id"] != selected_id
            ]
            st.success("Expense deleted successfully!")
            st.rerun()

    else:
        st.info(
            "No expenses recorded yet. Add your first expense above "
            "to see your analytics dashboard."
        )


# =====================================================
# FOOTER
# =====================================================

st.markdown(
    """
    <div class="footer">
        BankMate AI | Powered by Qwen3-4B + LoRA
        <br>
        AI-powered banking assistance
    </div>
    """,
    unsafe_allow_html=True,
)
