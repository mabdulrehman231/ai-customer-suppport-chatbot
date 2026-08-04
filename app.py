import pandas as pd
import streamlit as st
from chatbot import get_response
from config import APP_TITLE
from utils.database import (
    create_tables,
    save_message,
    load_chat_history,
    clear_chat_history,
    search_chat_history
)


st.set_page_config(
    page_title=APP_TITLE,
    page_icon="🤖",
    layout="wide"
)


st.markdown("""
<style>

.main > div{
    padding-top:1rem;
}

[data-testid="stSidebar"]{
    background:#0F172A;
}

[data-testid="stSidebar"] *{
    color:white;
}

.stChatMessage{
    border-radius:15px;
    padding:10px;
}

</style>
""", unsafe_allow_html=True)

create_tables()

import os
from utils.vector_store import create_vector_database

if not os.path.exists("database/chroma_db"):
    create_vector_database()
st.sidebar.title("ABC Electronics")
st.sidebar.caption("AI Customer Support")
st.sidebar.divider()
page = st.sidebar.radio(
    "Navigation",
    [
        "💬 Chat",
        "📜 Chat History",
        "ℹ About"
    ]
)
st.sidebar.divider()
st.sidebar.markdown("### 📊 System")
st.sidebar.success("🟢 Ollama Connected")
st.sidebar.info("Database: SQLite")
st.sidebar.info("Knowledge Base: ChromaDB")
st.sidebar.divider()
st.sidebar.caption("Version 1.0")


if page == "💬 Chat":
    st.title("🤖 AI Customer Support Assistant")
    st.caption(
        "Welcome to **ABC Electronics**. "
        "I'm here to help with products, refunds, shipping, warranties and more."
    )
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if len(st.session_state.messages) == 0:
        st.info("💡 Try one of these questions:")
        col1, col2 = st.columns(2)
        with col1:
            st.success("💻 Recommend a gaming laptop")
            st.success("💰 What is your refund policy?")
            st.success("🛡 Warranty for Gaming Laptop Pro?")
        with col2:
            st.success("🚚 Shipping policy")
            st.success("📧 Write a refund email")
            st.success("📦 Can I cancel my order?")
    for message in st.session_state.messages:
        avatar = "👤" if message["role"] == "user" else "🤖"
        with st.chat_message(message["role"], avatar=avatar):
            st.markdown(message["content"])
    prompt = st.chat_input("Ask me anything...")
    if prompt:
        st.session_state.messages.append(
            {
                "role":"user",
                "content":prompt
            }
        )
        save_message("user", prompt)
        with st.chat_message("user", avatar="👤"):
            st.markdown(prompt)
        with st.chat_message("assistant", avatar="🤖"):
            with st.spinner("Thinking..."):
                response = get_response(st.session_state.messages)
                if isinstance(response, dict):
                    st.markdown(response["answer"])
                    with st.expander("📄 View Company Policy Source"):
                        st.write(response["source"])
                else:
                    st.markdown(response)
                st.caption("source:Company policy")
        assistant_text = response["answer"] if isinstance(response, dict) else response
        st.session_state.messages.append(
            {
                "role": "assistant",
                "content": assistant_text
            }
        )
        save_message("assistant", assistant_text)


elif page == "📜 Chat History":
    st.title("📜 Chat History")
    search = st.text_input("🔍 Search Messages")
    col1, col2 = st.columns([1,1])
    with col1:
        if st.button("🗑 Clear History"):
            clear_chat_history()
            st.success("History Cleared")
            st.rerun()
    if search:
        history = search_chat_history(search)
    else:
        history = load_chat_history()

    if history:
        st.metric(
            "Total Messages",
            len(history)
        )
        df = pd.DataFrame(
            history,
            columns=[
                "ID",
                "Role",
                "Message",
                "Timestamp"
            ]
        )

        csv = df.to_csv(index=False).encode("utf-8")
        st.download_button(
            "⬇ Download CSV",
            csv,
            "chat_history.csv",
            "text/csv"
        )

        st.divider()
        for row in history:
            avatar = "👤" if row[1] == "user" else "🤖"
            with st.chat_message(
                row[1],
                avatar=avatar
            ):
                st.caption(row[3])
                st.write(row[2])

    else:
        st.info("No chat history found.")



elif page == "ℹ About":
    st.title("ℹ About")
    st.markdown("""
## 🤖 AI Customer Support Chatbot

An AI-powered customer support assistant that helps users with:

- 📦 Product Recommendations
- 💰 Refund Policies
- 🚚 Shipping Information
- 🛡 Warranty Details
- 📧 Email Generation
- 🛠 Complaint Handling
- 📚 Company Policy Search (RAG)
---
""")
    col1, col2 = st.columns(2)
    with col1:
        st.subheader("🛠 Technologies")
        st.write("🐍 Python")
        st.write("🎈 Streamlit")
        st.write("🦙 Ollama")
        st.write("📚 LangChain")
        st.write("🧠 ChromaDB")
        st.write("🗄 SQLite")
    with col2:
        st.subheader("✨ Features")
        st.write("✔ AI Chat")
        st.write("✔ RAG Search")
        st.write("✔ Chat History")
        st.write("✔ CSV Export")
        st.write("✔ Product Recommendation")
        st.write("✔ Complaint Support")

    st.divider()
    st.success("Developed by Your Name")
    st.caption("Version 1.0")