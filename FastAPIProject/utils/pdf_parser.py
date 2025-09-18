# utils/pdf_parser.py
import fitz  # PyMuPDF
import re


def extract_text_from_pdf(path: str) -> str:
    """
    Извлекает весь текст из PDF как строку.
    """
    doc = fitz.open(path)
    full_text = []
    for page in doc:
        txt = page.get_text("text")
        if txt:
            full_text.append(txt)
    return "\n".join(full_text)


def parse_pdf_hybrid(path: str):
    """
    Универсальный парсер PDF.
    Алгоритм:
    1) Если есть встроенное оглавление (TOC) → используем его.
    2) Если нет → ищем заголовки по визуальным признакам (шрифт/ключевые слова).
    3) Если нет → режем по регуляркам.
    4) Если совсем ничего → возвращаем весь текст одним куском.
    """
    doc = fitz.open(path)
    toc = doc.get_toc()
    chapters = []
    chapter_num = 1

    # 1) Пробуем встроенное оглавление (TOC)
    if toc:
        for i, (level, title, page_num) in enumerate(toc):
            start = page_num - 1
            end = toc[i + 1][2] - 1 if i + 1 < len(toc) else len(doc)

            text_parts = []
            for p in range(start, end):
                text_parts.append(doc[p].get_text("text"))

            chapters.append({
                "chapter_num": chapter_num,
                "title": title.strip(),
                "text": "\n".join(text_parts).strip()
            })
            chapter_num += 1
        return chapters

    # 2) Если TOC нет → визуальный поиск заголовков
    visual_chapters = []
    for page_index, page in enumerate(doc):
        blocks = page.get_text("dict")["blocks"]
        for b in blocks:
            for l in b.get("lines", []):
                for s in l.get("spans", []):
                    text = s["text"].strip()
                    if not text:
                        continue
                    # Заголовки обычно крупнее среднего или содержат ключевые слова
                    if s["size"] > 14 or text.upper().startswith(
                        ("БӨЛҮМ", "КИТЕП", "АРНОО", "ГЛАВА", "CHAPTER")
                    ):
                        visual_chapters.append((text, page_index))

    if visual_chapters:
        for i, (title, start_page) in enumerate(visual_chapters):
            end_page = (
                visual_chapters[i + 1][1] if i + 1 < len(visual_chapters) else len(doc)
            )
            text_parts = []
            for p in range(start_page, end_page):
                text_parts.append(doc[p].get_text("text"))
            chapters.append({
                "chapter_num": chapter_num,
                "title": title,
                "text": "\n".join(text_parts).strip()
            })
            chapter_num += 1
        return chapters

    # 3) Fallback — регулярки
    full_text = extract_text_from_pdf(path)
    pattern = re.compile(
        r'(^|\n)\s*((?:Бөлүм|Бөлүк|Китеп|Глава|Chapter)\s*[0-9IVXLC\-–]*)',
        flags=re.IGNORECASE | re.MULTILINE
    )
    matches = list(pattern.finditer(full_text))
    if matches:
        for i, m in enumerate(matches):
            start = m.end()
            end = matches[i + 1].start() if i + 1 < len(matches) else len(full_text)
            title = m.group(2).strip()
            chapter_text = full_text[start:end].strip()
            chapters.append({
                "chapter_num": chapter_num,
                "title": title,
                "text": chapter_text
            })
            chapter_num += 1
        return chapters

    # 4) Совсем fallback — один кусок текста
    return [{
        "chapter_num": 1,
        "title": None,
        "text": full_text
    }]


# Для обратной совместимости — alias
split_text_to_chapters = parse_pdf_hybrid
