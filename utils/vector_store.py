import chromadb
import ollama
from utils.pdf_loader import load_documents
from utils.text_splitter import split_documents

client = chromadb.PersistentClient(path="database/chroma_db")

collection = client.get_or_create_collection(
    name="company_policy"
)

def create_vector_database():
    documents = load_documents()
    chunks = split_documents(documents)
    try:
        client.delete_collection("company_policy")
    except:
        pass

    collection = client.get_or_create_collection(
        name="company_policy"
    )

    for i, chunk in enumerate(chunks):

        embedding = ollama.embeddings(
            model="all-minilm:latest",
            prompt=chunk.page_content
        )["embedding"]

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk.page_content]
        )

    print(" Vector Database Created Successfully!")