import faiss
import json
import numpy as np

def build_faiss_index(embeddings: np.ndarray, metadata: list, faiss_file: str, meta_file: str):
    dim = embeddings.shape[1]
    index = faiss.IndexFlatL2(dim)
    index.add(embeddings)
    faiss.write_index(index, faiss_file)
    with open(meta_file, "w", encoding="utf-8") as f:
        json.dump(metadata, f, ensure_ascii=False, indent=2)

def search(query_emb: np.ndarray, faiss_file: str, meta_file: str, book_name: str = None, top_k: int = 3):
    index = faiss.read_index(faiss_file)
    with open(meta_file, encoding="utf-8") as f:
        metadata = json.load(f)

    D, I = index.search(query_emb, top_k)

    results = []
    for idx in I[0]:
        if book_name is None or metadata[idx]["source"] == book_name:
            results.append(metadata[idx])
    return results

