from sentence_transformers import SentenceTransformer
import numpy as np

model = SentenceTransformer('sentence-transformers/LaBSE')

def embed_texts(texts):
    embeddings = model.encode(texts, convert_to_numpy=True, show_progress_bar=True)
    return embeddings
