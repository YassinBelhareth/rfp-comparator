from core.schema import RFPDoc

def test_rfpdoc_defaults():
    d = RFPDoc(doc_id="x")
    assert d.doc_id == "x"
