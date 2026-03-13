# models/embeddings.py
# Initializes the embedding model
# Only job: return a working embedding model object
# Embeddings convert text → numbers (vectors)

from langchain_community.embeddings import SentenceTransformerEmbeddings
from config.config import EMBEDDING_MODEL


def get_embedding_model():
    """
    Creates and returns a LangChain-compatible embedding model.
    
    WHAT ARE EMBEDDINGS?
    - Converts text into a list of numbers (vector)
    - Similar meaning = similar numbers = close in vector space
    - This is how RAG finds relevant chunks for a question
    
    WHY SentenceTransformerEmbeddings?
    - Runs 100% locally, no API key needed
    - LangChain-compatible (works directly with FAISS)
    - all-MiniLM-L6-v2 is fast, small, and accurate
    
    HOW TO EXTEND:
    - Better accuracy? Change to "all-mpnet-base-v2" in .env
    - Multilingual?    Change to "paraphrase-multilingual-MiniLM-L12-v2"
    - Use OpenAI?      Replace with OpenAIEmbeddings(api_key=...)
    """
    try:
        model = SentenceTransformerEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")