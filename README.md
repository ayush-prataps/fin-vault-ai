# FinVault AI

Minimal RAG system answering questions over SEC filings with page-level citations.

## Architecture

- Backend: FastAPI
- Vector store: PostgreSQL with pgvector (single table: `chunks`)
- Embeddings: `sentence-transformers` (`BAAI/bge-small-en-v1.5`)
- LLM: Groq API (`GROQ_MODEL` from environment, temperature 0)
- Frontend: Next.js single-page interface

## Endpoints

- `GET /health`
- `POST /query`: `{"question": "...", "tickers": ["..."], "year": 2023}` -> `{"answer": "...", "citations": [...], "model": "...", "latency_ms": 123, "tokens": 456}`

## Setup

### Backend

```bash
cd backend
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run build
npm run dev
```
