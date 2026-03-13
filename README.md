# 🤖 InsightBot — Intelligent Knowledge Assistant

> An AI-powered chatbot that understands your documents, searches the web in real-time, and responds intelligently using state-of-the-art LLMs.

Built as part of the **NeoStats AI Engineer Case Study**.

---

## 📌 Table of Contents

- [Overview](#overview)
- [App Screenshot](#-app-screenshot)
- [Features](#features)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [Configuration](#configuration)
- [Deployment](#deployment)
- [Challenges & Solutions](#challenges--solutions)

---

## Overview

InsightBot is a conversational AI assistant that solves a real-world problem: **users struggle to extract insights from large documents and lack access to real-time information in a single interface.**

InsightBot addresses this by combining three powerful capabilities:
1. **RAG (Retrieval-Augmented Generation)** — upload any PDF and ask questions about it
2. **Live Web Search** — search the internet in real-time when document context is unavailable
3. **Flexible Response Modes** — switch between concise and detailed responses on the fly

---

## 📸 App Screenshot

![InsightBot UI](screenshot.png)

> **Shown above:** InsightBot answering questions from an uploaded PDF resume in Detailed mode. The sidebar shows Response Mode toggle, Web Search toggle, PDF upload with 8 chunks loaded, and Clear Chat button.

---

## Features

### Mandatory Features
| Feature | Description |
|---|---|
| 📄 RAG Integration | Upload PDFs → extract text → chunk → embed → store in FAISS → retrieve by semantic similarity |
| 🌐 Live Web Search | Tavily API searches the web in real-time as a fallback when no document is uploaded |
| 🎛️ Response Modes | Sidebar toggle between **Concise** (2-3 sentences) and **Detailed** (full explanation) |

### Additional Features
| Feature | Description |
|---|---|
| ⛓️ LangChain Integration | Full LCEL chain using `ChatPromptTemplate`, `MessagesPlaceholder`, `StrOutputParser` |
| 💬 Multi-turn Chat History | Full conversation history maintained and sent to LLM on every turn |
| 🔒 Secure Config | API keys managed via `.env` locally and Streamlit Secrets on cloud — never hardcoded |

---

## Tech Stack

### Core AI & LLM
| Tool | Purpose |
|---|---|
| [Groq](https://console.groq.com) | LLM API provider — fast inference for LLaMA 3.3 70B |
| [LangChain](https://langchain.com) | LLM orchestration — chains, prompts, memory |
| `langchain-groq` | LangChain wrapper for Groq's ChatGroq model |
| `langchain-huggingface` | LangChain wrapper for HuggingFace embedding models |
| `langchain-text-splitters` | Smart recursive text chunking |
| `langchain-core` | Core LangChain primitives — messages, parsers, templates |

### RAG (Retrieval-Augmented Generation)
| Tool | Purpose |
|---|---|
| [FAISS](https://github.com/facebookresearch/faiss) | Vector similarity search — stores and retrieves embedded chunks |
| [SentenceTransformers](https://sbert.net) | Local embedding model — `all-MiniLM-L6-v2` converts text to vectors |
| [PyPDF2](https://pypdf2.readthedocs.io) | PDF text extraction |

### Web Search
| Tool | Purpose |
|---|---|
| [Tavily](https://tavily.com) | AI-optimized web search API — returns clean summaries, not raw HTML |

### Frontend & Deployment
| Tool | Purpose |
|---|---|
| [Streamlit](https://streamlit.io) | Python web app framework — chat UI, sidebar, file upload |
| [Streamlit Cloud](https://streamlit.io/cloud) | Free cloud deployment platform |

### Environment & Config
| Tool | Purpose |
|---|---|
| [python-dotenv](https://pypi.org/project/python-dotenv/) | Loads `.env` file into environment variables |
| GitHub | Version control and source hosting |

---

## Project Structure

```
InsightBot/
│
├── config/
│   └── config.py               # All settings and API keys via os.getenv()
│
├── models/
│   ├── llm.py                  # Groq LLM initialization via LangChain
│   └── embeddings.py           # SentenceTransformer embedding model
│
├── utils/
│   ├── __init__.py
│   ├── rag_utils.py            # PDF extraction, chunking, FAISS vector store, retrieval
│   └── search_utils.py         # Tavily live web search
│
├── app.py                      # Main Streamlit UI — connects all components
├── requirements.txt            # Python dependencies
├── packages.txt                # System dependencies for Streamlit Cloud (libgomp1)
├── .env                        # API keys — never committed to GitHub
├── .gitignore                  # Excludes .env, myenv/, __pycache__/
└── README.md
```

---

## Getting Started

### Prerequisites
- Python 3.9+
- Groq API key — [Get free key](https://console.groq.com)
- Tavily API key — [Get free key](https://app.tavily.com)

### 1. Clone the Repository
```bash
git clone https://github.com/shreebarse12/INSIGHTBOT-INTELLIGENT-KNOWLEDGE-ASSISTANT.git
cd INSIGHTBOT-INTELLIGENT-KNOWLEDGE-ASSISTANT
```

### 2. Install Dependencies
```bash
pip install -r requirements.txt
```

### 3. Set Up Environment Variables
Create a `.env` file in the project root:
```bash
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
TAVILY_API_KEY=your_tavily_api_key_here
EMBEDDING_MODEL=all-MiniLM-L6-v2
```

### 4. Run the App
```bash
streamlit run app.py
```

Open your browser at `http://localhost:8501`

---

## Configuration

All settings are managed in `config/config.py` and read from environment variables:

| Variable | Description | Default |
|---|---|---|
| `GROQ_API_KEY` | Groq API key for LLM access | Required |
| `GROQ_MODEL` | Groq model name | `llama-3.3-70b-versatile` |
| `TAVILY_API_KEY` | Tavily API key for web search | Required |
| `EMBEDDING_MODEL` | HuggingFace embedding model | `all-MiniLM-L6-v2` |
| `CHUNK_SIZE` | Characters per text chunk | `500` |
| `CHUNK_OVERLAP` | Overlap between chunks | `50` |
| `TOP_K_RESULTS` | Number of chunks to retrieve | `3` |

---

## How It Works

```
User asks a question
        ↓
PDF uploaded? → YES → Extract text → Chunk → Embed → FAISS index
        ↓
Retrieve top-K relevant chunks (semantic similarity)
        ↓
No chunks found + Web Search ON? → Tavily searches internet live
        ↓
Build system prompt with context + response mode instruction
        ↓
LangChain chain: PromptTemplate | ChatGroq | StrOutputParser
        ↓
Display response in Streamlit chat UI
```

---

## Deployment

The app is deployed on **Streamlit Cloud**.

### Steps to Deploy Your Own
1. Push code to GitHub (ensure `.env` is in `.gitignore`)
2. Go to [streamlit.io/cloud](https://streamlit.io/cloud)
3. Connect your GitHub repo
4. Set `app.py` as the entry point
5. Add secrets in **Settings → Secrets**:
```toml
GROQ_API_KEY = "your_key"
GROQ_MODEL = "llama-3.3-70b-versatile"
TAVILY_API_KEY = "your_key"
EMBEDDING_MODEL = "all-MiniLM-L6-v2"
```
6. Click **Deploy**

> **Note:** `packages.txt` contains `libgomp1` which is required for FAISS on Linux (Streamlit Cloud).

---

## Challenges & Solutions

| Challenge | Solution |
|---|---|
| `llama3-8b-8192` decommissioned mid-development | Switched to `llama-3.3-70b-versatile` |
| API key not loading — `config.py` imported before `load_dotenv()` ran | Moved `os.getenv()` inside functions, added `load_dotenv(override=True)` |
| LangChain import errors — modules moved between packages | Updated to `langchain-text-splitters`, `langchain-huggingface`, `langchain-core` |
| GitHub push rejected — `myenv/` (252MB) and `.env` in git history | Used `git filter-branch` to purge history, updated `.gitignore` |
| App worked locally but failed on Streamlit Cloud | Added all API keys in Streamlit Cloud Secrets section |
| FAISS failing on Linux (Streamlit Cloud) | Created `packages.txt` with `libgomp1` system dependency |

---

## 📄 License

This project was built for the NeoStats AI Engineer technical interview assignment.

---

*Built with ❤️ using Groq · LangChain · FAISS · Tavily · Streamlit*
