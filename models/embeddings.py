from langchain_community.embeddings import SentenceTransformerEmbeddings
from config.config import EMBEDDING_MODEL


def get_embedding_model():
    try:
        model = SentenceTransformerEmbeddings(
            model_name=EMBEDDING_MODEL
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")