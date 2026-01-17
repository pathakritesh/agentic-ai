import streamlit as st
import requests

API_URL = "http://127.0.0.1:8000/ask"

st.set_page_config(
    page_title="📄 PDF Chat",
    layout="centered"
)

st.title("📄 Chat with your PDFs")

if "chat" not in st.session_state:
    st.session_state.chat = []

question = st.text_input("Ask a question about your PDFs")

if st.button("Ask") and question.strip():
    response = requests.post(
        API_URL,
        json={"question": question}
    ).json()

    st.session_state.chat.append(
        ("You", question, [])
    )
    st.session_state.chat.append(
        ("Assistant", response["answer"], response.get("sources", []))
    )

# ---------------- DISPLAY CHAT ----------------

for role, message, sources in st.session_state.chat:
    st.markdown(f"**{role}:** {message}")

    if role == "Assistant" and sources:
        st.markdown("📚 **Sources:**")
        for src in sources:
            st.caption(
                f"📄 {src['file_name']} — page {src['page']}"
            )
