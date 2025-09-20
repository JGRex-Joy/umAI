import numpy as np
from sentence_transformers import SentenceTransformer

_model = SentenceTransformer("sentence-transformers/LaBSE")

def embed_texts(texts: list[str]):
    return _model.encode(texts, convert_to_numpy=True, show_progress_bar=False)
