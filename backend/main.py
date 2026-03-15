import os
from pathlib import Path

from dotenv import load_dotenv
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import chromadb

from llama_index.core import VectorStoreIndex, Settings
from llama_index.core.storage.storage_context import StorageContext
from llama_index.vector_stores.chroma import ChromaVectorStore
from llama_index.embeddings.openai import OpenAIEmbedding
from llama_index.llms.openai import OpenAI


load_dotenv()

app = FastAPI()


class AskRequest(BaseModel):
    question: str


BASE_DIR = Path(__file__).resolve().parent
DB_PATH = BASE_DIR / "storage" / "chroma_db"
COLLECTION_NAME = "mca_rules"


api_key = os.getenv("OPENAI_API_KEY")
if not api_key:
    raise ValueError("OPENAI_API_KEY not found. Put it in backend/.env")


# LLM + embedding configuration
Settings.embed_model = OpenAIEmbedding(model="text-embedding-3-small")
Settings.llm = OpenAI(model="gpt-4.1-mini")


# Connect to persisted Chroma DB
chroma_client = chromadb.PersistentClient(path=str(DB_PATH))
chroma_collection = chroma_client.get_collection(COLLECTION_NAME)

vector_store = ChromaVectorStore(chroma_collection=chroma_collection)
storage_context = StorageContext.from_defaults(vector_store=vector_store)


# THIS is what was missing
index = VectorStoreIndex.from_vector_store(
    vector_store=vector_store,
    storage_context=storage_context,
)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/debug-config")
def debug_config():
    return {
        "db_path": str(DB_PATH),
        "collection_name": COLLECTION_NAME,
        "openai_key_present": bool(api_key),
    }


@app.post("/ask")
def ask_question(request: AskRequest):
    try:
        query_engine = index.as_query_engine(similarity_top_k=5)

        prompt = f"""
You are an assistant for cricket umpiring league rules.
Answer only from the retrieved rule documents.
If the answer is not in the retrieved context, say:
"I could not find this in the league rules."

Question: {request.question}
"""

        response = query_engine.query(prompt)

        sources = []
        if hasattr(response, "source_nodes") and response.source_nodes:
            for node in response.source_nodes:
                sources.append(
                    {
                        "score": node.score,
                        "text": node.text[:400],
                        "metadata": node.metadata,
                    }
                )

        return {
            "question": request.question,
            "answer": str(response),
            "sources": sources,
        }

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
