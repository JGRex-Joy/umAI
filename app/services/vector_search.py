import faiss
import numpy as np
from pathlib import Path

BASE_DIR = Path(__file__).parent.parent.parent  
DATA_DIR = BASE_DIR / "data"
DATA_DIR.mkdir(exist_ok=True)
INDEX_PATH = DATA_DIR / "faiss.index"

def build_faiss_index(embeddings):
    embeddings = np.array(embeddings).astype("float32")
    faiss.normalize_L2(embeddings)
    dim = embeddings.shape[1]
    index = faiss.IndexFlatIP(dim)  
    index.add(embeddings)
    return index

def save_faiss_index(index, filename="faiss.index"):
    path = DATA_DIR / filename
    faiss.write_index(index, str(path))
    print(f"Saved FAISS index to {path}")

def load_faiss_index(filename="faiss.index"):
    path = DATA_DIR / filename
    if not path.exists():
        raise FileNotFoundError(f"FAISS index not found: {path}")
    return faiss.read_index(str(path))

def search(index, query_embedding, top_k=5):
    q = np.array([query_embedding]).astype("float32")
    faiss.normalize_L2(q)
    scores, ids = index.search(q, top_k)
    return ids[0], scores[0]
