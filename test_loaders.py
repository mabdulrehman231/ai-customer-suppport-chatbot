from utils.pdf_loader import load_documents
from utils.text_splitter import split_documents

documents = load_documents()

print("=" * 50)
print("Documents Loaded:", len(documents))

chunks = split_documents(documents)

print("Chunks Created:", len(chunks))
print("=" * 50)

for i, chunk in enumerate(chunks):
    print(f"\nChunk {i+1}")
    print("-" * 40)
    print(chunk.page_content)