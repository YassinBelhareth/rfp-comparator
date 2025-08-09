from typing import Dict, List
from .schema import RFPDoc, CompareRequest, CompareResult

DIMENSIONS = ["technical_requirements", "deliverables", "timeline", "eligibility", "budget"]

def _coverage(items: List[str]) -> float:
    if not items:
        return 0.0
    # proxy simple: + d'items -> meilleur (normalisé)
    return min(1.0, len(items) / 10.0)

def _timeline_score(timeline) -> float:
    # proxy: présence des 3 dates clés
    got = sum(bool(getattr(timeline, f)) for f in ["submission_deadline", "questions_deadline", "start_date"])
    return got / 3.0

def score_docs(req: CompareRequest) -> CompareResult:
    scores = {}
    breakdown = {}
    for d in req.docs:
        dims = {}
        dims["technical_requirements"] = _coverage(d.technical_requirements)
        dims["deliverables"] = _coverage(d.deliverables)
        dims["eligibility"] = _coverage(d.eligibility)
        dims["timeline"] = _timeline_score(d.timeline)
        budget_score = 1.0 if (d.budget_min or d.budget_max) else 0.0
        dims["budget"] = budget_score
        breakdown[d.doc_id] = dims
        scores[d.doc_id] = sum(dims[k] * req.weights.get(k, 0.0) for k in dims)
    lines = ["# RFP Comparison"]
    for doc_id, s in sorted(scores.items(), key=lambda x: -x[1]):
        parts = " ".join([f"{k}:{breakdown[doc_id][k]:.2f}" for k in DIMENSIONS])
        lines.append(f"- **{doc_id}** — score {s:.3f} ({parts})")
    summary = "\n".join(lines)
    return CompareResult(scores=scores, breakdown=breakdown, summary_md=summary)
