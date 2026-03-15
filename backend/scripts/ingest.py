import os
from dotenv import load_dotenv

from llama_index.core import SimpleDirectoryReader, VectorStoreIndex, Settings
from llama_index.core.node_parser import SentenceSplitter
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.core.storage.storage_context import StorageContext

import chromadb

def main():
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        raise ValueError("OPENAI_API_KEY not found in environment variables")

    Settings.embed_model = OpenAIEmbedding(model = "text-embedding-3-small")
    Settings.text_splitter = SentenceSplitter(
        chunk_size=500,
        chunk_overlap=80,
    )

    documents = SimpleDirectoryReader("data").load_data()

    chroma_client = chromadb.PersistentClient(path="storage/chroma_db")
    chroma_collection = chroma_client.get_or_create_collection(name="mca_rules")

    vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
    storage_context = StorageContext.from_defaults(vector_store=vector_store)

    VectorStoreIndex.from_documents(
        documents,
        storage_context=storage_context
    )

    print("Ingestion complete.")
    print(f"Loaded {len(documents)} page-level document(s) from PDF.")


if __name__ == "__main__":
    main()