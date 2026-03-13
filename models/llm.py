import os
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL

def get_chatgroq_model():
    try:
        model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")