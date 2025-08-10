# RFP Comparator · Intelligent Request for Proposal Comparison (LLM + RAG + PDF)

[![Python](https://img.shields.io/badge/Python-3.10+-blue.svg)](https://www.python.org/)
[![FastAPI](https://img.shields.io/badge/FastAPI-API-green)](https://fastapi.tiangolo.com/)
[![LLM](https://img.shields.io/badge/LLM-RAG-orange)](#)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![CI](https://github.com/YassinBelhareth/rfp-comparator/actions/workflows/ci.yml/badge.svg)](https://github.com/YassinBelhareth/rfp-comparator/actions)

---

This project automates the extraction and comparison of key information from 2–5 PDF RFP/RFQ documents.  
It uses a **LLM + RAG pipeline** to find relevant sections (budget, deliverables, technical requirements, deadlines, eligibility), extract them into a **standard JSON structure**, compute a **multi-criteria score**, and generate a **report** (Excel/Markdown).

---

## 🚀 Features
- **RAG retrieval**: Split PDF → chunks, create embeddings → find top-k relevant chunks for predefined questions.
- **Heuristic extraction by default**: No API key needed; local rules extract structured information.
- **Configurable scoring**: Weight technical requirements, deliverables, deadlines, eligibility, budget.
- **Report export**: Sorted Excel sheet + Markdown summary.
- **REST API**: Built with FastAPI, documented via `/docs`.
- **CI ready**: Pytest tests, GitHub Actions, Dockerfile.

---

## 🧠 Pipeline Overview
```
PDFs → split into chunks → embeddings → similarity search (per question)
     → heuristic extraction (default) or LLM extraction
     → normalized JSON (RFPDoc)
     → scoring → Excel/Markdown report
```

---

## ⚙️ LLM & Embeddings Configuration

- **Default embeddings**: Local `sentence-transformers/all-MiniLM-L6-v2` (offline, free).
- **Optional embeddings**: OpenAI `text-embedding-3-small` (requires API key).
- **Default extraction**: Heuristic rules (no API calls).
- **Optional extraction**: Use OpenAI GPT (`gpt-4o-mini`) or a local LLaMA model.

### Switch to OpenAI embeddings:
```bash
export EMBEDDINGS=openai
export OPENAI_API_KEY=sk-...
export OPENAI_EMBED_MODEL=text-embedding-3-small
```

### Switch to LLM extraction:
Edit `core/llm.py` to enable API calls.

---

## 📦 Installation & Quick Start

```bash
# 1. Create and activate virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run API
uvicorn api.main:app --reload
# Open http://127.0.0.1:8000/docs
```

---

## 🐳 Docker
```bash
docker build -t rfp-comparator .
docker run -p 8000:8000 rfp-comparator
```

---

## 📁 Providing your PDFs

The folder `data/samples/` is **empty** by default.  
To test the project:
1. Add 2–5 RFP PDFs (text-based or OCR processed) into `data/samples/`.
2. Start the API.
3. Use `/ingest` in Swagger docs to upload and process.

*Tip*: You can also provide `{doc_id, text}` JSON directly for testing without PDFs.

---

## 📊 Default Scoring Rules

| Dimension             | Rule (MVP)                                  | Weight |
|-----------------------|---------------------------------------------|-------:|
| Technical requirements| min(1, nb_items / 10)                       | 0.35  |
| Deliverables          | min(1, nb_items / 10)                       | 0.25  |
| Timeline              | completeness (questions/submission/start)/3 | 0.20  |
| Eligibility           | min(1, nb_items / 10)                       | 0.10  |
| Budget                | 1 if budget mentioned, else 0               | 0.10  |

> Advanced mode: `score = covered_requirements / total_requirements`

---

## 🧭 Roadmap

- Robust timeline/budget parsing (dates, currencies).
- LLM-based evaluation criteria extraction with citations.
- Vector database integration (FAISS/Weaviate).
- Simple front-end for PDF upload + live ranking.
- Multilingual RFP support.

---

## 📂 Project Structure

```
api/
  main.py         # API endpoints: /health, /ingest, /compare
core/
  extract.py      # PDF → raw text
  chunker.py      # Text → chunks
  embeddings.py   # Local or OpenAI embeddings
  retrieval.py    # Similarity search
  llm.py          # Heuristic or LLM extraction
  schema.py       # Pydantic models
  scoring.py      # Score calculation
  report.py       # Excel/Markdown export
data/
  samples/        # Place your PDFs here
tests/            # Pytest
Dockerfile, requirements.txt, pyproject.toml
```

---

## 👤 Author
**Yassin Belhareth** — AI/NLP Engineer.  
This project demonstrates a complete LLM + RAG pipeline applied to a real-world business case.
