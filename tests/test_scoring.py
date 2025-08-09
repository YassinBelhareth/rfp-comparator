from core.schema import RFPDoc, Timeline, CompareRequest
from core.scoring import score_docs

def test_scoring_basic():
    docs = [
        RFPDoc(doc_id="A", deliverables=["X"], technical_requirements=["Y"], timeline=Timeline()),
        RFPDoc(doc_id="B")
    ]
    res = score_docs(CompareRequest(docs=docs))
    assert res.scores["A"] >= res.scores["B"]
