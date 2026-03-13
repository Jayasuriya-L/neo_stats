import os
import sys

# sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from langchain_community.vectorstores import FAISS
from models.embeddings import get_embedding_model
from config.config import TOP_K_RESULTS


def create_vector_store(chunks):
    """Create a FAISS vector store from document chunks"""
    try:
        embeddings = get_embedding_model()
        vector_store = FAISS.from_documents(chunks, embeddings)
        return vector_store

    except Exception as e:
        raise RuntimeError(f"Failed to create vector store: {str(e)}")


def get_retriever(vector_store, k=TOP_K_RESULTS):
    """Return a retriever from an existing vector store"""
    return vector_store.as_retriever(search_kwargs={"k": k})
