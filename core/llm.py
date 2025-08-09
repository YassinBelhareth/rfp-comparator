import os
from typing import List, Dict
from pydantic import BaseModel

class Slot(BaseModel):
    name: str
    question: str

SLOTS = [
    Slot(name="deliverables", question="Liste précise des livrables attendus."),
    Slot(name="technical_requirements", question="Exigences techniques/stack/standards."),
    Slot(name="eligibility", question="Exigences d'éligibilité (qualifications, références)."),
    Slot(name="timeline", question="Dates clés (questions, soumission, démarrage)."),
    Slot(name="budget", question="Budget, fourchettes, devises, modalités."),
    Slot(name="evaluation_criteria", question="Critères d'évaluation et pondérations."),
]

USE_OPENAI = bool(os.getenv("OPENAI_API_KEY"))

def llm_extract(slot: Slot, contexts: List[Dict]) -> Dict:
    """MVP: heuristique simple (pas d'appel LLM requis).
    Concat top contexts et renvoie les lignes 'significatives'.
    """
    text = "\n\n".join(c["text"] for c in contexts)
    lines = [l.strip("- •* ") for l in text.split("\n") if len(l) > 5][:15]
    return {"slot": slot.name, "items": lines, "citations": contexts}
