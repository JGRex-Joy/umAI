from services.embedder import embed_texts
from services.vector_search import search
from services.gemini_client import ask_gemini

FAISS_FILE = "app/embeddings/index.faiss"
META_FILE = "app/embeddings/metadata.json"

def main():
    book = input("Манас / Сынган Кылыч: ").strip()
    
    query = input("Введите вопрос: ")
    query_emb = embed_texts([query])

    results = search(query_emb, FAISS_FILE, META_FILE, book_name=book, top_k=10)

    context = "\n".join([r["text"] for r in results])
    answer = ask_gemini(query, context)

    print("\n--- Ответ ---")
    print(answer)
    print("\n--- Чанки ---")
    for r in results:
        print(f"[{r['source']}] {r['text'][:150]}...")

if __name__ == "__main__":
    main()
