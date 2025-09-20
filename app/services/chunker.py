import re

def chunk_text(text: str, chunk_size: int = 300, overlap: int = 30):
    words = re.split(r'\s+', text)
    chunks, i, idx = [], 0, 0
    while i < len(words):
        chunk = words[i:i+chunk_size]
        chunks.append(" ".join(chunk))
        i += chunk_size - overlap
        idx += 1
    return chunks
