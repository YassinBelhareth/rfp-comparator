import pandas as pd
from .schema import CompareResult

def to_dataframe(res: CompareResult) -> pd.DataFrame:
    rows = []
    for doc_id, dims in res.breakdown.items():
        row = {"doc_id": doc_id, **dims, "score": res.scores[doc_id]}
        rows.append(row)
    return pd.DataFrame(rows).sort_values("score", ascending=False)

def export_excel(df: pd.DataFrame, path: str) -> str:
    df.to_excel(path, index=False)
    return path
