from fastapi import HTTPException
from sqlalchemy.orm import Session

from db_models import Work, Chapter


def get_all_works(db: Session):
    if(db.query(Work).first() is None):
        raise HTTPException(
            status_code=404, detail=f"No books in database"
        )
    else:
        return db.query(Work).all()

def get_chapter_text_from_work(work_id: int, chapter_number: int,  db: Session):
    if(db.query(Work).filter(Work.id == work_id).first() is None):
        raise HTTPException(
            status_code=404, detail=f"Book with id {work_id} not found"
        )
    if(db.query(Chapter).filter(Chapter.work_id == work_id, Chapter.chapter_num == chapter_number).first() is None):
        raise HTTPException(
            status_code=404, detail=f"Chapter with id {chapter_number} not found"
        )
    if(db.query(Chapter).filter(Chapter.work_id == work_id, Chapter.chapter_num == chapter_number).first().text is None):
        raise HTTPException(
            status_code=404, detail=f"Chapter with id {chapter_number} has no text"
        )
    else:
        return db.query(Chapter).filter(Chapter.work_id == work_id, Chapter.chapter_num == chapter_number).first()


