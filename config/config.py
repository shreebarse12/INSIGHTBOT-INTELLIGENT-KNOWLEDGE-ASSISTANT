# config/config.py
# Central place for all settings
# Every other file imports from here
# To change any setting, change it here only

import os
from dotenv import load_dotenv

# load_dotenv() reads .env file and loads all variables
# MUST be called before any os.getenv() calls
load_dotenv()

# ── LLM Settings ──────────────────────────
GROQ_API_KEY = os.getenv("GROQ_API_KEY")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama3-8b-8192")

# ── Embedding Settings ─────────────────────
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# ── Web Search Settings ────────────────────
TAVILY_API_KEY = os.getenv("TAVILY_API_KEY")

# ── RAG Settings ───────────────────────────
# CHUNK_SIZE: how many characters per chunk
# CHUNK_OVERLAP: shared characters between chunks
# TOP_K_RESULTS: how many chunks to retrieve
CHUNK_SIZE = 500
CHUNK_OVERLAP = 50
TOP_K_RESULTS = 3