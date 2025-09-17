from app.services.chunks_manager import load_docx, split_into_chunks, save_chunks
from app.services.embeddings import embed_texts
import faiss
import numpy as np
from pathlib import Path

DOC_PATH = "works/manas.docx"

FULL_TEXT, PARAGRAPHS = load_docx(DOC_PATH)

CHUNKS = split_into_chunks(PARAGRAPHS)
save_chunks(CHUNKS)

texts = [c["text"] for c in CHUNKS]
print(f"[DEBUG] Начало эмбеддинга {len(texts)} чанков")
embeddings = embed_texts(texts).astype("float32")
print(f"[DEBUG] Эмбеддинги созданы: shape={embeddings.shape}")

dim = embeddings.shape[1]
index = faiss.IndexFlatL2(dim)
index.add(embeddings)
print(f"[DEBUG] FAISS индекс создан, количество векторов: {index.ntotal}")

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)
faiss.write_index(index, str(DATA_DIR / "faiss.index"))
print(f"[DEBUG] FAISS индекс сохранён: {DATA_DIR / 'faiss.index'}")

print("[DEBUG] Всё готово!")
