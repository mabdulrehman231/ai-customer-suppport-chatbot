import chromadb
from sentence_transformers import SentenceTransformer

from utils.pdf_loader import load_documents
from utils.text_splitter import split_documents

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# ChromaDB client
client = chromadb.PersistentClient(path="database/chroma_db")

collection = client.get_or_create_collection(
    name="company_policy"
)


def create_vector_database():

    documents = load_documents()

    chunks = split_documents(documents)

    # Delete old collection
    try:
        client.delete_collection("company_policy")
    except:
        pass

    collection = client.get_or_create_collection(
        name="company_policy"
    )

    # Create embeddings
    for i, chunk in enumerate(chunks):

        embedding = embedding_model.encode(
            chunk.page_content
        ).tolist()

        collection.add(
            ids=[str(i)],
            embeddings=[embedding],
            documents=[chunk.page_content]
        )

    print(" Vector Database Created Successfully!")