from core.extract import extract_chunks

def test_extract_chunks_smoke():
    assert callable(extract_chunks)
