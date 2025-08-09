# RFP Comparator · Compareur intelligent d'appels d'offres (LLM + RAG + PDF)

Automatise l'extraction d'informations clés depuis 2–5 PDF (RFP/RFQ), produit un JSON normalisé,
calcule un score multi-critères, et génère un rapport (Excel/Markdown).

## Démarrage rapide
```bash
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
uvicorn api.main:app --reload
# Ouvrir http://127.0.0.1:8000/docs
```
