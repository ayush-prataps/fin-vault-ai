# FinVault AI

Smallest honest RAG pipeline answering questions over real SEC filings with page-level citations and measured benchmark numbers.

## Architecture

1. Client: Vanilla HTML/CSS/JavaScript interface served directly by FastAPI.
2. API: FastAPI exposing GET /health, GET /corpus, and POST /query endpoints.
3. Chunker: Page-aware PDF parser slicing original text (zero decode artifacts) with structural table preservation up to 800 tokens, header repetition across split rows, and context headers prepended to embedding inputs.
4. Embeddings: BAAI/bge-small-en-v1.5 running locally via fastembed (ONNX Runtime, zero PyTorch).
5. Vector Database: PostgreSQL with pgvector extension storing chunk vectors and metadata.
6. Retrieval: Top-k cosine similarity search with optional ticker and year SQL filters.
7. Context Formatter: Numbered bracket citations [1], [2] containing document, year, and page.
8. Generation: OpenAI-compatible LLM client supporting dual providers (DeepSeek `deepseek-flash` in non-thinking mode and Groq `qwen/qwen3.8-27b`) with prefix routing, automatic failover, temperature 0.0, timeout, `max_tokens`, and provider-isolated response caching. Questions and retrieved filing excerpts are sent to a third-party LLM API.
9. Guardrails: Explicit abstention prompt when context lacks required facts; zero mock data.
10. Evaluation: Automated FinanceBench harness testing retrieval hit rate and answer accuracy.

## How to Run

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements.txt
python scripts/download_model.py
python scripts/ingest_corpus.py
uvicorn app.main:app --reload
```

Open [http://localhost:8000](http://localhost:8000) in your browser.

## How to Reproduce Evaluation

Run the evaluation script against the 150 FinanceBench questions:

```bash
python eval/run_eval.py
```

Results JSON files are written with full timestamped logs under `eval/results/`.

## Embedding Engine Benchmark (Measured)

Measured on Apple Silicon (`BAAI/bge-small-en-v1.5`, 384 dimensions):

| Metric | SentenceTransformers (PyTorch) | FastEmbed (ONNX Runtime) | Measured Change |
|---|---|---|---|
| Virtualenv Disk Size | 1,200 MB | 239 MB | -80.1% |
| Peak RSS (Model Load + 1st Query) | 540.73 MB | 216.70 MB | -59.9% |
| 1st Query Cold Load Time | 3.63s | 0.06s | -98.3% |
| 100 Query Embedding Time | 0.5513s (5.51 ms/query) | 0.3155s (3.16 ms/query) | -42.8% |
| Cosine Similarity to Stored Vectors (N=100) | 1.000000 | Min: 0.999998, Mean: 0.999999, Max: 0.999999 | 99.9999% identical |

## Benchmark Results (Full FinanceBench: 150 Questions, 84 Filings, 32 Companies)

Measured across all 150 questions in FinanceBench against 32,289 chunks from 84 SEC filings:

| Metric | Config A: Unfiltered Baseline | Config B: Pipeline (Company Filter) |
|---|---|---|
| Retrieval Hit Rate @ 5 | 32.67% (49/150) | 34.67% (52/150) |
| Retrieval Hit Rate @ 10 | 38.67% (58/150) | 40.67% (61/150) |

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
