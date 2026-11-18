# FinVault AI

Smallest honest RAG pipeline answering questions over real SEC filings with page-level citations and measured benchmark numbers.

## Architecture

1. Client: Next.js single-page application submitting natural language queries.
2. API: FastAPI exposing GET /health and POST /query endpoints.
3. Chunker: Page-aware PDF parser preserving structural table boundaries at ~400 tokens.
4. Embeddings: BAAI/bge-small-en-v1.5 running locally via sentence-transformers.
5. Vector Database: PostgreSQL with pgvector extension storing chunk vectors and metadata.
6. Retrieval: Top-k cosine similarity search with optional ticker and year SQL filters.
7. Context Formatter: Numbered bracket citations [1], [2] containing document, year, and page.
8. Generation: Groq API running qwen/qwen3.8-27b with temperature 0.0.
9. Guardrails: Explicit abstention prompt when context lacks required facts; zero mock data.
10. Evaluation: Automated FinanceBench harness testing retrieval hit rate and answer accuracy.

## How to Run

### Backend

```bash
cd backend
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/ingest_corpus.py
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## How to Reproduce Evaluation

Run the evaluation script against the 31 FinanceBench questions:

```bash
cd backend
python eval/run_eval.py
```

Results JSON files are written with full timestamped logs under `backend/eval/results/`.

## Benchmark Results

Evaluated on 31 FinanceBench questions across 8 SEC 10-K and 10-Q filings (3M, AMD, American Express, Boeing) on commit `73bd4b6467bfa039bb14727b9b9d9ca4d6dd74c1` using `qwen/qwen3.8-27b`.

| Metric | Overall (31 questions) | Numeric (14 questions) | Narrative (17 questions) |
|---|---|---|---|
| Retrieval Hit Rate @ 5 (no filter) | 22.58% (7/31) | 21.43% (3/14) | 23.53% (4/17) |
| Retrieval Hit Rate @ 10 (no filter) | 25.81% (8/31) | 35.71% (5/14) | 23.53% (4/17) |
| Retrieval Hit Rate @ 5 (ticker filter) | 22.58% (7/31) | 21.43% (3/14) | 23.53% (4/17) |
| Retrieval Hit Rate @ 10 (ticker filter) | 29.03% (9/31) | 35.71% (5/14) | 23.53% (4/17) |
| Answer Accuracy (top-5 context) | 25.81% (8/31) | 28.57% (4/14) | 23.53% (4/17) |
| Abstention Rate | 64.52% (20/31) | 64.29% (9/14) | 64.71% (11/17) |
| Incorrect Answer Rate | 9.68% (3/31) | 7.14% (1/14) | 11.76% (2/17) |

## Known Limitations

Observed failure modes from the benchmark run:

1. Cross-year semantic collision displacing target tables:
   In `financebench_id_03029` (3M FY2018 capex), the question asks for 2018 cash flow statement figures. Without an explicit year filter, generic semantic overlap on "capital expenditure" causes 2022 and 2023 filings to rank higher than 2018 page 59. The model honestly abstains because the 2018 table is absent from top-5 context.

2. Multi-segment disclosure truncation:
   In `financebench_id_00995` (AMD FY2022 major products), the filing lists server microprocessors, GPUs, DPUs, and semi-custom SoCs across multiple pages. Top-5 retrieval retrieved only the first page, resulting in an incomplete product list.

3. Reporting segment taxonomy versus geographical lists:
   In `financebench_id_01028` (American Express principal geographies), the model retrieved country-level and global office counts from the business description rather than the four internal operating segments ("United States, EMEA, APAC, LACC").

4. Enterprise-level consolidation versus segment disclosures:
   In `financebench_id_01290` (Boeing primary customers), the retrieved excerpts broke down defense and commercial customers by division, but missed the consolidated footnote stating the US Government accounted for 40% of total revenue.
