import numpy as np
from typing import List, Dict
from .embeddings import embed

class Retriever:
    def __init__(self, windows: List[Dict]):
        self.windows = windows
        self.vecs = embed([w["text"] for w in windows])
        self.mat = np.vstack(self.vecs)
        self.mat = self.mat / np.linalg.norm(self.mat, axis=1, keepdims=True)

    def topk(self, query: str, k: int = 5) -> List[Dict]:
        q = embed([query])[0]
        q = q / np.linalg.norm(q)
        sims = self.mat @ q
        idx = np.argsort(-sims)[:k]
        return [{**self.windows[i], "score": float(sims[i])} for i in idx]
