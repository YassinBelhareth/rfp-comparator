from pydantic import BaseModel, Field
from typing import List, Optional, Dict

class Citation(BaseModel):
    page: int
    text: str
    bbox: Optional[List[float]] = None  # [x0, y0, x1, y1]

class Criterion(BaseModel):
    name: str
    value: Optional[str] = None
    weight: Optional[float] = None
    citations: List[Citation] = []

class Timeline(BaseModel):
    submission_deadline: Optional[str] = None  # ISO date
    questions_deadline: Optional[str] = None
    start_date: Optional[str] = None

class RFPDoc(BaseModel):
    doc_id: str
    title: Optional[str] = None
    client: Optional[str] = None
    currency: Optional[str] = None
    budget_min: Optional[float] = None
    budget_max: Optional[float] = None
    deliverables: List[str] = []
    technical_requirements: List[str] = []
    eligibility: List[str] = []
    evaluation_criteria: List[Criterion] = []
    timeline: Timeline = Timeline()
    risks: List[str] = []

class CompareRequest(BaseModel):
    docs: List[RFPDoc]
    weights: Dict[str, float] = Field(default_factory=lambda: {
        "technical_requirements": 0.35,
        "deliverables": 0.25,
        "timeline": 0.20,
        "eligibility": 0.10,
        "budget": 0.10,
    })

class CompareResult(BaseModel):
    scores: Dict[str, float]
    breakdown: Dict[str, Dict[str, float]]  # doc_id -> dimension -> score
    summary_md: str
