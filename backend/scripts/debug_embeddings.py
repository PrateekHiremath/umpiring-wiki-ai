import chromadb

client = chromadb.PersistentClient(path="storage/chroma_db")

collection = client.get_collection("mca_rules")

results = collection.get(include=["embeddings", "documents"])

embeddings = results["embeddings"]
documents = results["documents"]

print(f"Total embeddings: {len(embeddings)}\n")

for i in range(min(5, len(embeddings))):
    print(f"Embedding {i+1}:")

    vector = embeddings[i]

    print(f"Vector length: {len(vector)}")
    print(f"First 10 numbers: {vector[:10]}")

    print("\nAssociated chunk text:")
    print(documents[i][:300])

    print("\n-----------------------------\n")