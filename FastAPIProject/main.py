import os

from db_models import Work, Chapter
import shutil
from datetime import datetime

from fastapi import FastAPI, Depends, UploadFile, File, HTTPException
from sqlalchemy.orm import Session

import database
import db_models
from database import engine
from pydantic_models import WorkBase, WorkOut
import Service as service
from utils.pdf_parser import extract_text_from_pdf, parse_pdf_hybrid
from utils.remover_of_links import remove_all_links

app = FastAPI()

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

db_models.Base.metadata.create_all(bind=engine)



def get_db():
    db = database.SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.get("/")
def greet():
    return {"yokoso, uzar gay"}

@app.get("/works")
def get_works_endpoint(db: Session = Depends(get_db)):
    if(db.query(Work).first() is None):
        raise HTTPException(
            status_code=404, detail=f"No books in database"
        )
    else:
        return service.get_all_works(db)

@app.get("/works/{work_id}/chapters")
def get_chapters_endpoint(work_id: int, db: Session = Depends(get_db)):
    if(db.query(Work).filter(Work.id == work_id).first() is None):
        raise HTTPException(
            status_code=404, detail=f"Book with id {work_id} not found"
        )
    if(db.query(Chapter).filter(Chapter.work_id == work_id).first() is None):
        raise HTTPException(
            status_code=404, detail=f"No chapters in book with id {work_id}"
        )
    else:
        return db.query(Chapter).filter(Chapter.work_id == work_id).all()

@app.post("/api/upload_book_pdf/", response_model=WorkOut)
async def upload_pdf_and_clean(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """
    Загружает PDF, удаляет ссылки, сохраняет файл, создаёт запись в базе и разбивает на главы.
    """
    original_name = file.filename or "document.pdf"
    base, ext = os.path.splitext(original_name)
    if (ext or "").lower() != ".pdf":
        raise HTTPException(status_code=400, detail="Загрузите PDF-файл.")

    input_path = os.path.join(UPLOAD_DIR, original_name)
    with open(input_path, "wb") as f:
        shutil.copyfileobj(file.file, f)

    output_name = f"{base}-.pdf"
    output_path = os.path.join(UPLOAD_DIR, output_name)

    try:
        remove_all_links(input_path, output_path)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Ошибка удаления ссылок: {e}")

    full_text = extract_text_from_pdf(output_path)
    if not full_text.strip():
        raise HTTPException(status_code=400, detail="Не удалось извлечь текст из PDF после очистки ссылок.")

    existing = db.query(Work).filter(Work.title == original_name).first()
    if existing:
        existing.file_path = output_path
        existing.created_at = datetime.utcnow()
        db.commit()
        db.refresh(existing)
        work = existing
    else:
        work = Work(
            title=original_name,
            author=None,
            description=None,
            file_path=output_path,
            created_at=datetime.utcnow(),
        )
        db.add(work)
        db.commit()
        db.refresh(work)

    chapters = parse_pdf_hybrid(output_path)
    for c in chapters:
        chap = Chapter(
            work_id=work.id,
            chapter_num=c["chapter_num"],
            title=c.get("title"),
            text=c["text"]
        )
        db.add(chap)
        db.commit()
        db.refresh(chap)

    return work

@app.get("/works/{work_id}/chapters/{chapter_number}")
def get_chapter_text(work_id: int, chapter_number: int, db: Session = Depends(get_db)):
    return service.get_chapter_text_from_work(work_id,chapter_number, db)


