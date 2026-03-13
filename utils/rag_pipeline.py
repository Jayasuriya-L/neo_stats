import os
import sys

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from utils.document_loader import load_documents
from utils.text_splitter import split_documents
from utils.vector_store import create_vector_store, get_retriever


def build_rag_pipeline(file_paths):
    """
    End-to-end RAG pipeline:
      1. Load documents from file paths
      2. Split into chunks
      3. Embed and store in FAISS
      4. Return a retriever
    """
    try:
        documents = load_documents(file_paths)

        if not documents:
            raise ValueError("No documents were loaded. Check the uploaded files.")

        chunks = split_documents(documents)
        vector_store = create_vector_store(chunks)
        retriever = get_retriever(vector_store)
        return retriever

    except Exception as e:
        raise RuntimeError(f"Failed to build RAG pipeline: {str(e)}")


def retrieve_context(retriever, query):
    """Retrieve relevant document chunks for a query and return as a single string"""
    try:
        docs = retriever.invoke(query)
        context = "\n\n".join([doc.page_content for doc in docs])
        return context

    except Exception as e:
        return f"Error retrieving context: {str(e)}"
