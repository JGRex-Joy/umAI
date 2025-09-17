def build_prompt(chunks, query):
    context = "\n\n".join(c["text"] for c in chunks)
    return f"Контекст:\n{context}\n\nСуроо:\n{query}\n\nЖооп бериңиз:"
