import os
from langchain_community.document_loaders import PyPDFLoader, TextLoader


def load_documents(file_paths):
    """Load documents from a list of file paths (PDF or TXT supported)"""
    documents = []

    for path in file_paths:
        try:
            ext = os.path.splitext(path)[-1].lower()

            if ext == ".pdf":
                loader = PyPDFLoader(path)
            elif ext == ".txt":
                loader = TextLoader(path, encoding="utf-8")
            else:
                print(f"Unsupported file type '{ext}' for file: {path}")
                continue

            docs = loader.load()
            documents.extend(docs)

        except Exception as e:
            print(f"Error loading '{path}': {str(e)}")

    return documents
