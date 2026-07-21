import chromadb
import ollama

client = chromadb.PersistentClient(path="database/chroma_db")

collection = client.get_collection("company_policy")


def retrieve_context(query, top_k=3):

    response = ollama.embeddings(
        model="all-minilm:latest",
        prompt=query
    )

    results = collection.query(
        query_embeddings=[response["embedding"]],
        n_results=top_k
    )

    documents = results["documents"][0]

    context = "\n\n".join(documents)

    return context