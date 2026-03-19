# Umpiring wiki AI - Backend

A backend AI service for a cricket umoiring rules assistant

This project uses a Retreival-Augmented Generation (RAG) pipeline to answer league-specific umpiring questions from a PDF rulebook. The current implementation loads a pdf documents, splits it into chunks, generates embeddings for each chunk, stores them in a Chroma vector database, and exposes an API endpoint to answer questions using stored knowledge base.

## Features

- Load cricket league rulebook from PDF
- Split document into chunks for retreival
- Generate embeddings using OpenAI
- Store embeddings in Chroma vector database.
- Ask questions through a FastAPI endpoint.
- Return grounded answers with retreived source chunks.

## Tech Stack

- Python 3.11
- FastAPI
- LlamaIndex
- OpenAI Embeddings + LLM
- ChromaDB
- PyPDF

## Project Structure

umpiring-wiki-ai/
└── backend/
    ├── data/
    │   └── mca_rules.pdf
    ├── scripts/
    │   ├── ingest.py
    │   ├── debug_chunks.py
    │   └── debug_embeddings.py
    ├── storage/
    │   └── chroma_db/
    ├── .env
    ├── .gitignore
    ├── main.py
    ├── requirements.txt
    └── README.md

## Prerequisites (For Mac)

Install the following on your Mac:
Python 3.11
Git
OpenAI API key

Recommended:
VS Code
Homebrew

Check installed versions:
python3.11 --version
git --version


## Setup Instructions : 

1. Clone the repository
git clone <your-github-repo-url>
cd umpiring-wiki-ai/backend

2. Create a Python virtual environment
python3.11 -m venv .venv
source .venv/bin/activate

Verify: 
python --version

Expected: 
Python 3.11.x

3. Install dependencies
pip install -r requirements.txt

If needed, install these explicitly:
pip install llama-index-vector-stores-chroma
pip install llama-index-embeddings-openai
pip install llama-index-readers-file
pip install llama-index-llms-openai

4. Add environment variables
Create a .env file inside backend/:
OPENAI_API_KEY=your_openai_api_key_here
Do not commit this file to GitHub.

5. Add the PDF rulebook
Put your rulebook PDF inside the data/ folder.

Example:
backend/data/mca_rules.pdf

## Build the Vector Database

Run the ingestion script:
python scripts/ingest.py

This will:
load the PDF
split it into chunks
generate embeddings
store them in ChromaDB under storage/chroma_db

If you want a clean rebuild, delete the local vector DB first:

rm -rf storage/chroma_db
python scripts/ingest.py

## Run the Backend API

Start the FastAPI server:
uvicorn main:app --reload

Server will run at:
http://127.0.0.1:8000

Swagger docs:
http://127.0.0.1:8000/docs

Health check:
http://127.0.0.1:8000/health

Debug config:
http://127.0.0.1:8000/debug-config

## API Endpoints : 

GET /health

Checks whether the server is running.
Response:
{
  "status": "ok"
}

GET /debug-config

Returns current backend configuration details such as DB path, collection name, and whether the OpenAI key is present.

POST /ask

Answers a question using retrieved rulebook chunks.
Example request:
{
  "question": "What is the rule for a no ball?"
}

Example response:
{
  "question": "What is the rule for a no ball?",
  "answer": "A no ball is called when ...",
  "sources": [
    {
      "score": 0.82,
      "text": "A bowler shall be deemed to have delivered a no ball if ...",
      "metadata": {
        "page_label": "8",
        "file_name": "mca_rules.pdf"
      }
    }
  ]
}

## Debugging Scripts : 

Inspect chunks

python scripts/debug_chunks.py

Inspect embeddings

python scripts/debug_embeddings.py

These are useful for validating the RAG pipeline and checking what text is stored in the vector DB.












