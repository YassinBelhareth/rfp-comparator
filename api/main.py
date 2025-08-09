from fastapi import FastAPI, UploadFile, File
from fastapi.middleware.cors import CORSMiddleware
from typing import List
import uuid

from core.extract import extract_chunks
from core.chunker import window_chunks
from core.retrieval import Retriever
from core.llm import SLOTS, llm_extract
from core.schema import RFPDoc, CompareRequest
from core.scoring import score_docs
from core.report import to_dataframe, export_excel

app = FastAPI(title="RFP Comparator")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

@app.get("/health")
def health():
    return {"status": "ok"}

@app.post("/ingest")
async def ingest(files: List[UploadFile] = File(...)):
    docs = []
    for f in files:
        path = f"/tmp/{uuid.uuid4()}_{f.filename}"
        with open(path, "wb") as w:
            w.write(await f.read())
        chunks = extract_chunks(path)
        if not chunks:
            # Empty fallback to avoid crashes
            chunks = [{"page": 1, "text": f.filename, "tag": "body"}]
        windows = window_chunks(chunks)
        retr = Retriever(windows)
        fields = {}
        for slot in SLOTS:
            ctx = retr.topk(slot.question, k=5)
            fields[slot.name] = llm_extract(slot, ctx).get("items", [])
        doc = RFPDoc(
            doc_id=f.filename,
            deliverables=fields.get("deliverables", []),
            technical_requirements=fields.get("technical_requirements", []),
            eligibility=fields.get("eligibility", []),
            # timeline/budget/eval_criteria à enrichir dans les itérations suivantes
        )
        docs.append(doc)
    return {"docs": [d.model_dump() for d in docs]}

@app.post("/compare")
async def compare(req: CompareRequest):
    res = score_docs(req)
    df = to_dataframe(res)
    path = export_excel(df, "/tmp/rfp_compare.xlsx")
    return {"result": res.model_dump(), "excel_path": path}
