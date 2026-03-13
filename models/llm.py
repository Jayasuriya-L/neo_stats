import os
import sys

# Add project root to path so config can be imported
# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_groq import ChatGroq
from config.config import GROQ_API_KEY, GROQ_MODEL


def get_chatgroq_model():
    """Initialize and return the Groq chat model using config settings"""
    try:
        if not GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is not set. "
                "Add it to your .env file or set it as an environment variable."
            )

        groq_model = ChatGroq(
            api_key=GROQ_API_KEY,
            model=GROQ_MODEL,
        )
        return groq_model

    except Exception as e:
        raise RuntimeError(f"Failed to initialize Groq model: {str(e)}")
