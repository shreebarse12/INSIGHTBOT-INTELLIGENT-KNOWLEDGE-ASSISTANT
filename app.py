# app.py
# Main Streamlit UI
# Connects all pieces together:
# LLM + RAG + Web Search + Response Modes

import streamlit as st
from dotenv import load_dotenv

# Load .env FIRST before anything else
load_dotenv()

from models.llm import get_chatgroq_model
from models.embeddings import get_embedding_model
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.prompts import ChatPromptTemplate, MessagesPlaceholder
from langchain_core.output_parsers import StrOutputParser
from utils.rag_utils import (
    extract_text_from_pdf,
    chunk_text,
    build_vector_store,
    retrieve_relevant_chunks
)
from utils.search_utils import web_search

# ── Page Setup ────────────────────────────────────────
st.set_page_config(
    page_title="LegalBot ⚖️",
    page_icon="⚖️",
    layout="wide"
)

st.title("⚖️ LegalBot — AI Legal Document Assistant")
st.caption("Upload a legal document and ask questions, or search the web.")


# ── Helper: Convert messages to LangChain format ──────
def convert_messages(messages: list) -> list:
    """
    Converts Streamlit dict messages to LangChain message objects.
    
    Streamlit stores: {"role": "user", "content": "Hello"}
    LangChain needs:  HumanMessage(content="Hello")
    """
    result = []
    for msg in messages:
        role = msg.get("role", "")
        content = msg.get("content", "")
        try:
            if role == "user":
                result.append(HumanMessage(content=content))
            elif role == "assistant":
                result.append(AIMessage(content=content))
        except Exception as e:
            print(f"[MESSAGE ERROR] {e}")
    return result


# ── Helper: Get LLM Response ──────────────────────────
def get_response(messages: list, system_prompt: str) -> str:
    """
    Builds prompt + runs LangChain chain + returns response string.
    
    Uses get_chatgroq_model() from models/llm.py
    Chain: prompt_template | llm | StrOutputParser
    """
    try:
        llm = get_chatgroq_model()

        prompt_template = ChatPromptTemplate.from_messages([
            ("system", "{system_prompt}"),
            MessagesPlaceholder(variable_name="chat_history"),
        ])

        # pipe operator: prompt → llm → parse to string
        chain = prompt_template | llm | StrOutputParser()

        response = chain.invoke({
            "system_prompt": system_prompt,
            "chat_history": convert_messages(messages),
        })

        return response
    except Exception as e:
        print(f"[LLM ERROR] {e}")
        return f"Error: {str(e)}"


# ── Sidebar ───────────────────────────────────────────
with st.sidebar:
    st.header("⚙️ Settings")

    # Response Mode
    # Changes how the system prompt instructs the LLM
    response_mode = st.radio(
        "📝 Response Mode",
        ["Concise", "Detailed"],
        help="Concise = 2-3 sentences. Detailed = full explanation."
    )

    # Web Search Toggle
    use_web_search = st.toggle(
        "🌐 Enable Web Search",
        value=False,
        help="Search web when no document is uploaded"
    )

    st.markdown("---")

    # PDF Upload
    uploaded_file = st.file_uploader(
        "📄 Upload Document (PDF)",
        type=["pdf"]
    )

    st.markdown("---")

    # Status
    if "vector_store" in st.session_state:
        st.success(f"✅ {st.session_state['chunk_count']} chunks loaded")
    else:
        st.info("No document loaded")

    # Clear chat
    if st.button("🗑️ Clear Chat"):
        st.session_state.messages = []
        st.rerun()


# ── PDF Processing ────────────────────────────────────
if uploaded_file is not None:
    # Only process if it's a new file
    if st.session_state.get("loaded_file") != uploaded_file.name:
        with st.spinner("Processing document..."):
            try:
                text = extract_text_from_pdf(uploaded_file)
                if not text:
                    st.sidebar.error("Could not extract text from PDF")
                else:
                    documents = chunk_text(text)
                    vector_store = build_vector_store(documents)

                    st.session_state["vector_store"] = vector_store
                    st.session_state["chunk_count"] = len(documents)
                    st.session_state["loaded_file"] = uploaded_file.name

                    st.sidebar.success(f"✅ {len(documents)} chunks indexed!")
            except Exception as e:
                st.sidebar.error(f"Error: {e}")


# ── Chat History ──────────────────────────────────────
if "messages" not in st.session_state:
    st.session_state.messages = []

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])


# ── Chat Input ────────────────────────────────────────
if prompt := st.chat_input("Ask anything..."):

    # Show user message
    with st.chat_message("user"):
        st.markdown(prompt)
    st.session_state.messages.append({"role": "user", "content": prompt})

    # Step 1: Try RAG first
    context = ""
    context_source = ""

    if "vector_store" in st.session_state:
        context = retrieve_relevant_chunks(
            prompt,
            st.session_state["vector_store"]
        )
        if context:
            context_source = "📄 Based on your uploaded document"

    # Step 2: Fall back to web search
    if use_web_search and not context:
        with st.spinner("🌐 Searching web..."):
            context = web_search(prompt)
            if context:
                context_source = "🌐 Based on live web search"

    # Step 3: Build system prompt based on response mode
    if response_mode == "Concise":
        mode_instruction = (
            "Give a SHORT and CONCISE answer. "
            "Maximum 2-3 sentences. Get straight to the point."
        )
    else:
        mode_instruction = (
            "Give a DETAILED and THOROUGH answer. "
            "Use bullet points or sections if it helps clarity."
        )

    system_prompt = f"""You are LegalBot, an intelligent AI legal assistant.
{mode_instruction}
If context is provided below, use it to answer accurately.
If no context is available, answer from your general knowledge.
Always suggest consulting a real lawyer for serious legal matters.

{'Context:' if context else 'No context available.'}
{context}"""

    # Step 4: Get response
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = get_response(
                st.session_state.messages,
                system_prompt
            )

        if context_source:
            st.caption(context_source)
        st.markdown(response)

    st.session_state.messages.append({
        "role": "assistant",
        "content": response
    })