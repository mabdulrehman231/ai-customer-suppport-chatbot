import chromadb
from sentence_transformers import SentenceTransformer

embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

client = chromadb.PersistentClient(path="database/chroma_db")

try:
    collection = client.get_collection("company_policy")
except:
    from utils.vector_store import create_vector_database
    create_vector_database()
    collection = client.get_collection("company_policy")


def retrieve_context(query, top_k=3):

    query_embedding = embedding_model.encode(query).tolist()

    results = collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k
    )

    documents = results["documents"][0]

    return "\n\n".join(documents)