import os
import json
import numpy as np
from pathlib import Path
from services.docx_loader import load_docx
from services.chunker import chunk_text
from services.embedder import embed_texts
from services.vector_search import build_faiss_index

DOCS = {
    "Манас": "app/data/manas.docx",
    "Сынган Кылыч": "app/data/syngan_kylych.docx"
}
OUTPUT_DIR = "embeddings"
FAISS_FILE = f"{OUTPUT_DIR}/index.faiss"
META_FILE = f"{OUTPUT_DIR}/metadata.json"

def build_corpus():
    corpus = []
    global_id = 0
    for book_name, path in DOCS.items():
        text = load_docx(path)
        chunks = chunk_text(text)
        for c in chunks:
            corpus.append({
                "id": global_id,
                "text": c,
                "source": book_name
            })
            global_id += 1
    return corpus

if __name__ == "__main__":
    print("📖 Создание корпуса…")
    corpus = build_corpus()
    print(f"✅ Чанков: {len(corpus)}")

    print("🔎 Эмбеддинги…")
    texts = [c["text"] for c in corpus]
    embeddings = embed_texts(texts)

    print("💾 Сохраняем…")
    Path(OUTPUT_DIR).mkdir(parents=True, exist_ok=True)
    build_faiss_index(embeddings, corpus, FAISS_FILE, META_FILE)

    print("🎉 Готово! index.faiss + metadata.json сохранены.")
