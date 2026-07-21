from utils.retriever import retrieve_context

query = "Can I cancel my order?"

context = retrieve_context(query)

print("=" * 50)
print(context)
print("=" * 50)