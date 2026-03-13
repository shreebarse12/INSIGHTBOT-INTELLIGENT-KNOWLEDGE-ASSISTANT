# models/llm.py
# Initializes the Groq LLM
# Only job: return a working LLM object
# Nothing else — no prompts, no messages here

import os
from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL


def get_chatgroq_model():
    """
    Creates and returns a LangChain ChatGroq LLM object.
    
    WHY LANGCHAIN WRAPPER?
    - Standard interface across all LLM providers
    - Swap to OpenAI/Gemini by changing just this function
    - Works with LangChain chains, prompts, memory
    
    HOW TO EXTEND:
    - Add temperature=0.7 for more creative responses
    - Add streaming=True for word by word output
    - Swap ChatGroq for ChatOpenAI to use OpenAI
    """
    try:
        model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
        )
        return model
    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")