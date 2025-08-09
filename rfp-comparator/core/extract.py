import pdfplumber
from typing import List, Dict

HEADING_HINTS = [
    "introduction", "scope", "deliverables", "eligibility",
    "evaluation", "timeline", "budget", "penalties", "criteria"
]

def extract_chunks(pdf_path: str) -> List[Dict]:
    chunks: List[Dict] = []
    with pdfplumber.open(pdf_path) as pdf:
        for i, page in enumerate(pdf.pages, start=1):
            text = page.extract_text() or ""
            if not text.strip():
                continue
            # naive split by double newline
            for para in text.split("\n\n"):
                t = para.strip()
                if not t:
                    continue
                tag = "body"
                low = t.lower()
                if any(h in low for h in HEADING_HINTS):
                    tag = "heading_or_section"
                chunks.append({
                    "page": i,
                    "text": t,
                    "tag": tag,
                })
    return chunks
