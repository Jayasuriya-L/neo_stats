# NEO Stats AI ChatBot

An intelligent conversational AI application built with Python and Streamlit, powered by Groq LLMs. The chatbot supports **Retrieval-Augmented Generation (RAG)** from local documents, **live web search**, and two response modes — Concise and Detailed.

---

## Features

| Feature | Description |
|---|---|
| **LLM Integration** | Powered by Groq (llama-3.3-70b-versatile by default) |
| **RAG** | Upload PDF or TXT files and chat with your documents |
| **Web Search** | Real-time DuckDuckGo search for up-to-date answers |
| **Response Modes** | Toggle between Concise and Detailed answers |
| **Modular Architecture** | Clean separation of config, models, and utilities |

---

## Project Structure

```
project/
│
├── app.py                  # Main Streamlit application
│
├── config/
│   └── config.py           # API keys and app configuration (loaded from .env)
│
├── models/
│   ├── llm.py              # Groq LLM integration
│   └── embeddings.py       # HuggingFace embedding model for RAG
│
├── utils/
│   ├── document_loader.py  # Load PDF and TXT files
│   ├── text_splitter.py    # Split documents into chunks
│   ├── vector_store.py     # FAISS vector store creation and retrieval
│   ├── rag_pipeline.py     # End-to-end RAG pipeline
│   └── web_search.py       # DuckDuckGo web search
│
├── requirements.txt        # Python dependencies
├── .env.example            # Environment variable template
└── .gitignore
```

---

## Tech Stack

- **Frontend** — [Streamlit](https://streamlit.io)
- **LLM Provider** — [Groq](https://groq.com) via `langchain-groq`
- **Embeddings** — [HuggingFace](https://huggingface.co) `all-MiniLM-L6-v2` (runs locally, no API key needed)
- **Vector Store** — [FAISS](https://github.com/facebookresearch/faiss)
- **Orchestration** — [LangChain](https://www.langchain.com)
- **Web Search** — [DuckDuckGo Search](https://pypi.org/project/duckduckgo-search/) (no API key needed)
- **Document Loaders** — `pypdf` for PDF, built-in for TXT

---

## Getting Started

### 1. Clone the repository

```bash
git clone https://github.com/Jayasuriya-L/neo_stats.git
cd neo_stats
```

### 2. Create a virtual environment

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# macOS / Linux
source venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure your API key

Copy the example environment file and add your Groq API key:

```bash
cp .env.example .env
```

Edit `.env`:

```
GROQ_API_KEY=your_groq_api_key_here
```

Get your free Groq API key from [https://console.groq.com/keys](https://console.groq.com/keys)

### 5. Run the app

```bash
streamlit run app.py
```

---

## Configuration

All settings are managed in `config/config.py` and loaded from the `.env` file.

| Variable | Default | Description |
|---|---|---|
| `GROQ_API_KEY` | — | **Required.** Your Groq API key |
| `GROQ_MODEL` | `llama-3.3-70b-versatile` | Groq model to use |
| `EMBEDDING_MODEL` | `all-MiniLM-L6-v2` | HuggingFace embedding model |
| `CHUNK_SIZE` | `500` | Document chunk size for RAG |
| `CHUNK_OVERLAP` | `50` | Overlap between chunks |
| `TOP_K_RESULTS` | `3` | Number of chunks retrieved per query |
| `MAX_SEARCH_RESULTS` | `3` | Number of web search results to fetch |

---

## Available Groq Models

| Model | Notes |
|---|---|
| `llama-3.3-70b-versatile` | Best quality — **default** |
| `llama-3.1-70b-versatile` | Large, capable |
| `llama-3.1-8b-instant` | Fastest response |
| `gemma2-9b-it` | Google Gemma 2 |

To switch models, update `GROQ_MODEL` in your `.env` file — no code changes needed.

---

## How to Use

### Chat
Type any question in the chat input box and press Enter.

### RAG — Chat with your documents
1. In the sidebar, go to **Upload Documents (RAG)**
2. Upload one or more PDF or TXT files
3. Click **Process Documents**
4. The chatbot will now answer questions using your document content

### Web Search
Toggle **Enable Web Search** in the sidebar. The chatbot will fetch real-time results from DuckDuckGo and include them in its answer.

### Response Modes
- **Concise** — Short, direct answers
- **Detailed** — Thorough explanations with examples

---

## Deployment on Streamlit Cloud

1. Push your code to a GitHub repository (ensure `.env` is in `.gitignore`)
2. Go to [https://streamlit.io/cloud](https://streamlit.io/cloud) and connect your repository
3. Set your secrets under **App Settings → Secrets**:

```toml
GROQ_API_KEY = "your_groq_api_key_here"
```

4. Deploy — Streamlit Cloud will install `requirements.txt` automatically

---

## Security

- **Never commit your `.env` file** — it is listed in `.gitignore`
- API keys are loaded exclusively through environment variables
- For cloud deployment, use Streamlit Secrets or your platform's secret manager

---

## License

This project is for educational purposes.
