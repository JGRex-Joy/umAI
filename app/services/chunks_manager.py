from pathlib import Path
import json
from docx import Document

DATA_DIR = Path("data")
DATA_DIR.mkdir(exist_ok=True)

CHUNKS_FILE = DATA_DIR / "chunks.json"

def load_docx(path: str):
    print(f"[DEBUG] Загружаем DOCX: {path}")
    doc = Document(path)
    paragraphs = [p.text.strip() for p in doc.paragraphs if p.text.strip()]
    print(f"[DEBUG] Всего абзацев: {len(paragraphs)}")
    full_text = "\n".join(paragraphs)
    return full_text, paragraphs

def split_into_chunks(paragraphs, book_name="unknown", max_tokens=512, overlap=50, start_id=0):
    print(f"[DEBUG] Разбиваем на чанки: max_tokens={max_tokens}, overlap={overlap}")
    chunks, current, length = [], [], 0
    chunk_id = start_id

    for i, para in enumerate(paragraphs, 1):
        words = para.split()
        if length + len(words) > max_tokens:
            chunks.append({
                "id": chunk_id,
                "book": book_name,
                "text": " ".join(current)
            })
            chunk_id += 1
            if overlap > 0 and len(current) > overlap:
                current = current[-overlap:]
                length = len(current)
            else:
                current, length = [], 0
        current.extend(words)
        length += len(words)

        if i % 50 == 0:
            print(f"[DEBUG] Обработано {i}/{len(paragraphs)} абзацев, чанков создано: {len(chunks)}")

    if current:
        chunks.append({
            "id": chunk_id,
            "book": book_name,
            "text": " ".join(current)
        })

    print(f"[DEBUG] Всего чанков создано: {len(chunks)}")
    return chunks

def save_chunks(chunks, append=False):
    if append and CHUNKS_FILE.exists():
        with open(CHUNKS_FILE, "r", encoding="utf-8") as f:
            old_chunks = json.load(f)
        chunks = old_chunks + chunks

    with open(CHUNKS_FILE, "w", encoding="utf-8") as f:
        json.dump(chunks, f, ensure_ascii=False, indent=2)

    print(f"[DEBUG] Чанки сохранены в {CHUNKS_FILE}")

def load_chunks(path: str = CHUNKS_FILE):
    print(f"[DEBUG] Загружаем чанки из {path}")
    with open(path, "r", encoding="utf-8") as f:
        chunks = json.load(f)
    print(f"[DEBUG] Загружено чанков: {len(chunks)}")
    return chunks
