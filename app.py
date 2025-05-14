import streamlit as st
import os
from utils.document_parser import parse_document
from utils.embed_store import embed_document
from utils.retriever import retrieve_context
from utils.gpt_handler import get_gpt_response
from utils.history_saver import save_history
from utils.session_manager import list_sessions, save_session, load_session, delete_session, create_new_session
from utils.title_generator import generate_title

# Page config
st.set_page_config(page_title="Psychiatrist Assistant", layout="wide")

# Load external CSS (must exist in static/style.css)
with open("static/style.css") as f:
    st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# JS for copy buttons (optional)
st.markdown("""
<script>
function copyToClipboard(id, btn) {
    const text = document.getElementById(id).innerText;
    navigator.clipboard.writeText(text).then(function() {
        btn.innerText = "✅ Copied!";
        setTimeout(() => { btn.innerText = "📋 Copy"; }, 2000);
    });
}
</script>
""", unsafe_allow_html=True)

# Handle query param to load chat session
if "load_session" in st.query_params:
    filename = st.query_params["load_session"]
    data = load_session(filename)
    st.session_state.chat_history = data["history"]
    st.session_state.chat_title = data["title"]
    st.session_state.current_session = filename
    st.query_params.clear()
    st.rerun()

# Session state init
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []
if "custom_prompt" not in st.session_state:
    st.session_state.custom_prompt = "You are a helpful clinical assistant."
if "current_session" not in st.session_state:
    st.session_state.current_session = None
if "chat_title" not in st.session_state:
    st.session_state.chat_title = None

# Sidebar
with st.sidebar:
    if st.button("🆕 New"):
        st.session_state.chat_history = []
        st.session_state.chat_title = None
        st.session_state.current_session = create_new_session()

    st.markdown("### 📂 History")
    for session in list_sessions():
        is_active = st.session_state.current_session == session["filename"]
        btn_class = "active-chat-btn" if is_active else "inactive-chat-btn"

        col1, col2 = st.columns([0.85, 0.15])
        with col1:
            st.markdown(
                f"""
                <form action="" method="get">
                    <input type="hidden" name="load_session" value="{session['filename']}"/>
                    <button class="{btn_class}" type="submit">{session['title']}</button>
                </form>
                """,
                unsafe_allow_html=True,
            )
        with col2:
            if st.button("🗑", key=f"del_{session['filename']}", use_container_width=True):
                delete_session(session["filename"])
                st.rerun()

    st.markdown("### 📎 Upload Docs")
    with st.expander("Upload (.pdf, .docx, .txt)", expanded=False):
        uploaded_file = st.file_uploader("Choose", type=["pdf", "docx", "txt"])
        if uploaded_file:
            with st.spinner("Embedding..."):
                text = parse_document(uploaded_file)
                embed_document(text, file_name=uploaded_file.name)
            st.success("✅ Embedded!")

    st.markdown("### ⚙️ Settings")
    custom = st.text_area("Prompt", value=st.session_state.custom_prompt, height=80)
    mode = st.radio("Mode", ["GPT", "Docs only", "Hybrid (GPT + Docs)"], index=2)

    if st.button("🧹 Clear"):
        st.session_state.chat_history = []
        st.success("✅ Cleared")
    if custom != st.session_state.custom_prompt:
        st.session_state.custom_prompt = custom
        st.success("💾 Saved")

# Chat Display
for idx, (role, message) in enumerate(st.session_state.chat_history):
    css_class = "user-msg" if role == "user" else "bot-msg"
    st.markdown(f"""
    <div class='chat-container {css_class}'>
        {message}
    </div>
""", unsafe_allow_html=True)

# Chat Input
if prompt := st.chat_input("Ask a clinical or research question..."):
    st.session_state.chat_history.append(("user", prompt))

    if not st.session_state.chat_title:
        st.session_state.chat_title = generate_title(prompt)

    with st.spinner("Thinking..."):
        context_chunks = []
        if mode != "GPT":
            context_chunks = retrieve_context(prompt, k=5)
        answer = get_gpt_response(prompt, context_chunks, mode, st.session_state.custom_prompt)

    st.session_state.chat_history.append(("assistant", answer))

    if st.session_state.current_session:
        save_session(
            st.session_state.current_session,
            st.session_state.chat_title,
            st.session_state.chat_history
        )

    save_history(prompt, answer)
    st.rerun()
