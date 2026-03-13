import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# --- Groq Configuration ---
GROQ_API_KEY = os.getenv("GROQ_API_KEY", "")
GROQ_MODEL = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")

# --- Embedding Configuration ---
EMBEDDING_MODEL = os.getenv("EMBEDDING_MODEL", "all-MiniLM-L6-v2")

# --- RAG Configuration ---
CHUNK_SIZE = int(os.getenv("CHUNK_SIZE", "500"))
CHUNK_OVERLAP = int(os.getenv("CHUNK_OVERLAP", "50"))
TOP_K_RESULTS = int(os.getenv("TOP_K_RESULTS", "3"))

# --- Web Search Configuration ---
MAX_SEARCH_RESULTS = int(os.getenv("MAX_SEARCH_RESULTS", "3"))
