import traceback
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from app.services.embedder import embed_texts
from app.services.vector_search import search
from app.services.gemini_client import ask_gemini

FAISS_FILE = "app/embeddings/index.faiss"
META_FILE = "app/embeddings/metadata.json"

app = FastAPI(title="Startup Nation API", version="1.0")

class Query(BaseModel):
    question: str

@app.post("/ask")
def ask(query: Query):
    try:
        query_emb = embed_texts([query.question])
        results = search(query_emb, FAISS_FILE, META_FILE, top_k=15)
        context = "\n".join([r["text"] for r in results])
        answer = ask_gemini(query.question, context)
        return {"answer": answer}
    except Exception as e:
        print("Ошибка в /ask:")
        traceback.print_exc()  
        raise HTTPException(status_code=500, detail=str(e))
