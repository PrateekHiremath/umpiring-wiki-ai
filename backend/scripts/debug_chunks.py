import chromadb
"""
This file is used to print out chunks.

This script connects to a ChromaDB persistent client, retrieves the 'mca_rules' collection,
fetches all documents (chunks), and prints the total number of chunks along with the first
300 characters of the first 5 chunks for debugging purposes.
"""

client = chromadb.PersistentClient(path="storage/chroma_db")

collection = client.get_collection("mca_rules")

results = collection.get()

documents = results["documents"]

print(f"Total chunks: {len(documents)}\n")

for i, doc in enumerate(documents[:5]):
    print(f"Chunk {i+1}:")
    print(doc[:300])
    print("\n--------------------\n")