import os
import sys

# Add project root to path so config can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.embeddings import HuggingFaceEmbeddings
from config.config import EMBEDDING_MODEL


def get_embedding_model():
    """Initialize and return a HuggingFace embedding model (runs locally, no API key needed)"""
    try:
        embeddings = HuggingFaceEmbeddings(
            model_name=EMBEDDING_MODEL,
            model_kwargs={"device": "cpu"},
            encode_kwargs={"normalize_embeddings": True},
        )
        return embeddings

    except Exception as e:
        raise RuntimeError(f"Failed to initialize embedding model: {str(e)}")
