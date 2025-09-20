from fastapi import FastAPI
from pydantic import BaseModel
from services.embedder import embed_texts
from services.vector_search import search
from services.gemini_client import ask_gemini

FAISS_FILE = "embeddings/index.faiss"
META_FILE = "embeddings/metadata.json"

app = FastAPI()

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    query_emb = embed_texts([query.question])
    results = search(query_emb, FAISS_FILE, META_FILE, top_k=3)
    context = "\n".join([r["text"] for r in results])
    answer = ask_gemini(query.question, context)
    return {"answer": answer, "chunks": results}
