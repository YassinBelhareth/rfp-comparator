# RFP Comparator · Intelligent Request for Proposal Comparison (LLM + RAG + PDF)

This project automates the extraction and comparison of key information from 2–5 PDF RFP/RFQ documents.  
It uses a **LLM + RAG pipeline** to find relevant sections (budget, deliverables, technical requirements, deadlines, eligibility), extract them into a **standard JSON structure**, compute a **multi-criteria score**, and generate a **report** (Excel/Markdown).

---

## 🚀 Features
- **RAG retrieval**: Split PDF → chunks, create embeddings → find top-k relevant chunks for predefined questions.
- **LLM or heuristic extraction**: Clean and normalize data into a JSON format.
- **Configurable scoring**: Weight technical requirements, deliverables, deadlines, eligibility, budget.
- **Report export**: Sorted Excel sheet + Markdown summary.
- **REST API**: Built with FastAPI, documented via `/docs`.
- **CI ready**: Pytest tests, GitHub Actions, Dockerfile.

---

## 🧠 Architecture


- **PDF parsing**: `pdfplumber` (text-based PDFs).
- **Embeddings**:  
  - Local: `sentence-transformers/all-MiniLM-L6-v2` (offline, free).  
  - Optional: OpenAI `text-embedding-3-small`.
- **LLM**:
  - Default: heuristic (no API calls).  
  - Optional: `gpt-4o-mini` (OpenAI) or local LLaMA for structured extraction.
- **Scoring**: Simple rules in MVP, customizable for real business needs.

---

## ⚙️ Configuration

**Local embeddings (default)**  
No API key required.

**OpenAI embeddings (optional)**
```bash
export EMBEDDINGS=openai


# 1. Create and activate virtual environment
python -m venv .venv && source .venv/bin/activate

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run API
uvicorn api.main:app --reload
# Open http://127.0.0.1:8000/docs

docker build -t rfp-comparator .
docker run -p 8000:8000 rfp-comparator
export OPENAI_API_KEY=sk-...
export OPENAI_EMBED_MODEL=text-embedding-3-small
