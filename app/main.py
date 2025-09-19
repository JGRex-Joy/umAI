# main.py
from pathlib import Path
import json
from app.services.embeddings import embed_texts
from app.services.vector_search import load_faiss_index, search
from app.utils.prompt_builder import build_prompt
from app.services.hf_client import generate_with_context
from app.services.chunks_manager import load_chunks

# --- Параметры ---
TOP_K = 3  # сколько ближайших чанков использовать для контекста

# Загружаем чанки и индекс
CHUNKS = load_chunks()
INDEX = load_faiss_index()

# Ввод запроса от пользователя
query = input("Введите вопрос: ")

# Создаём эмбеддинг запроса
query_emb = embed_texts([query])[0]

# Ищем top_k ближайших чанков
ids, scores = search(INDEX, query_emb, top_k=TOP_K)
selected_chunks = [CHUNKS[i] for i in ids]

# Формируем prompt
prompt = build_prompt(selected_chunks, query)

# Генерируем ответ через HF модель
answer = generate_with_context(context=prompt, query="")  # query уже в prompt

print("\n--- Ответ модели ---")
print(answer)
