import os
from typing import List

_PROVIDER = os.getenv("EMBEDDINGS", "local")

if _PROVIDER == "openai":
    from openai import OpenAI  # type: ignore
    client = OpenAI()
else:
    from sentence_transformers import SentenceTransformer  # type: ignore
    _model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

def embed(texts: List[str]):
    if _PROVIDER == "openai":
        # pseudo-code; adaptez selon SDK
        resp = client.embeddings.create(
            model=os.getenv("OPENAI_EMBED_MODEL", "text-embedding-3-small"),
            input=texts
        )
        return [d.embedding for d in resp.data]
    return _model.encode(texts, normalize_embeddings=True)
