import fitz
import re

def remove_all_links(input_path: str, output_path: str):
    """
    Убирает все ссылки из PDF (www.*, *.kg, http/https), сохраняя кириллицу и текст.
    """
    doc = fitz.open(input_path)

    # Шаблон для любых ссылок: www.* , http(s)://*, и *.kg
    link_pattern = re.compile(r'\b(?:https?://|www\.)\S+|\b\w+\.kg\b', re.IGNORECASE)

    for page in doc:
        # Удаляем кликабельные ссылки (аннотации)
        for annot in page.annots() or []:
            if annot.type[0] == 1:
                annot.delete()

        # Убираем ссылки прямо в тексте через редактирование блоков
        blocks = page.get_text("blocks")
        for b in blocks:
            x0, y0, x1, y1, text, *_ = b
            new_text = link_pattern.sub("", text)
            if new_text != text:
                # Замещаем текст в блоке через редактирование (без ломки кириллицы)
                page.add_redact_annot([x0, y0, x1, y1], fill=(1,1,1))
                page.apply_redactions()
                page.insert_textbox(
                    (x0, y0, x1, y1),
                    new_text,
                    fontsize=12,
                    fontname="Times-Roman",
                    align=0
                )

    doc.save(output_path)
    print(f"Все ссылки удалены. Новый PDF: {output_path}")
