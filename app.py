import streamlit as st
import os
import sys
import tempfile

# sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

from langchain_core.messages import HumanMessage, AIMessage, SystemMessage
from models.llm import get_chatgroq_model
from utils.rag_pipeline import build_rag_pipeline, retrieve_context
from utils.web_search import web_search


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def build_system_prompt(mode, rag_context=None, web_context=None):
    if mode == "Concise":
        base = (
            "You are a helpful AI assistant. "
            "Provide short, direct, and concise answers. "
            "Avoid unnecessary explanations."
        )
    else:
        base = (
            "You are a helpful AI assistant. "
            "Provide detailed, thorough, and well-explained answers. "
            "Include relevant examples and context where helpful."
        )

    if rag_context:
        base += "\n\nUse the following document context to answer the question:\n" + rag_context

    if web_context:
        base += "\n\nUse the following real-time web search results to supplement your answer:\n" + web_context

    return base


def get_chat_response(chat_model, messages, system_prompt):
    try:
        formatted_messages = [SystemMessage(content=system_prompt)]

        for msg in messages[:-1]:
            if msg["role"] == "user":
                formatted_messages.append(HumanMessage(content=msg["content"]))
            else:
                formatted_messages.append(AIMessage(content=msg["content"]))

        formatted_messages.append(HumanMessage(content=messages[-1]["content"]))

        response = chat_model.invoke(formatted_messages)
        return response.content

    except Exception as e:
        return f"Error getting response: {str(e)}"


# ---------------------------------------------------------------------------
# Main app
# ---------------------------------------------------------------------------

def main():
    st.set_page_config(
        page_title=" NEO Stats AI ChatBot",
        layout="wide",
        initial_sidebar_state="expanded",
    )

    st.title("NEO Stats AI ChatBot")

    # --- Sidebar ---
    with st.sidebar:
        st.header("Settings")

        # Response mode
        st.subheader("Response Mode")
        response_mode = st.radio(
            "Choose response style:",
            ["Concise", "Detailed"],
            index=0,
        )

        st.divider()

        # Web search
        st.subheader("Web Search")
        enable_web_search = st.toggle("Enable Web Search", value=False)

        st.divider()

        # RAG document upload
        st.subheader("Upload Documents (RAG)")
        uploaded_files = st.file_uploader(
            "Upload PDF or TXT files",
            type=["pdf", "txt"],
            accept_multiple_files=True,
        )

        if uploaded_files:
            if st.button("Process Documents", use_container_width=True):
                with st.spinner("Building vector index..."):
                    try:
                        temp_paths = []
                        for uf in uploaded_files:
                            suffix = os.path.splitext(uf.name)[-1]
                            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                                tmp.write(uf.read())
                                temp_paths.append(tmp.name)

                        retriever = build_rag_pipeline(temp_paths)
                        st.session_state.retriever = retriever
                        st.success(f"Processed {len(uploaded_files)} document(s)!")

                        for path in temp_paths:
                            try:
                                os.unlink(path)
                            except OSError:
                                pass

                    except Exception as e:
                        st.error(f"Error processing documents: {str(e)}")

        if st.session_state.get("retriever"):
            st.info("Documents loaded and ready.")
            if st.button("Clear Documents", use_container_width=True):
                st.session_state.retriever = None
                st.rerun()

        st.divider()

        # Clear chat
        if st.button(" Clear Chat History", use_container_width=True):
            st.session_state.messages = []
            st.rerun()

    # --- Initialize model ---
    try:
        chat_model = get_chatgroq_model()
    except Exception as e:
        st.error(f"**Model initialization failed:** {str(e)}\n\nCheck your GROQ_API_KEY in the `.env` file.")
        return

    # --- Session state ---
    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "retriever" not in st.session_state:
        st.session_state.retriever = None

    # --- Display chat history ---
    for message in st.session_state.messages:
        with st.chat_message(message["role"]):
            st.markdown(message["content"])

    # --- Chat input ---
    if prompt := st.chat_input("Type your message here..."):

        st.session_state.messages.append({"role": "user", "content": prompt})
        with st.chat_message("user"):
            st.markdown(prompt)

        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):

                # RAG retrieval
                rag_context = None
                if st.session_state.retriever:
                    try:
                        rag_context = retrieve_context(st.session_state.retriever, prompt)
                    except Exception as e:
                        st.warning(f"RAG retrieval failed: {str(e)}")

                # Web search
                web_context = None
                if enable_web_search:
                    try:
                        web_context = web_search(prompt)
                    except Exception as e:
                        st.warning(f"Web search failed: {str(e)}")

                # Build prompt and get response
                system_prompt = build_system_prompt(response_mode, rag_context, web_context)
                response = get_chat_response(chat_model, st.session_state.messages, system_prompt)
                st.markdown(response)

        st.session_state.messages.append({"role": "assistant", "content": response})


if __name__ == "__main__":
    main()
