import os
from langchain_community.document_loaders import (
    PyPDFLoader,
    TextLoader
)

DOCS_PATH = "docs"

def load_documents():
    documents = []

    for filename in os.listdir(DOCS_PATH):
        filepath = os.path.join(DOCS_PATH, filename)

        if filename.endswith(".pdf"):
            loader = PyPDFLoader(filepath)
            documents.extend(loader.load())

        elif filename.endswith(".txt"):
            loader = TextLoader(filepath, encoding="utf-8")
            documents.extend(loader.load())

    return documents