from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class WorkBase(BaseModel):
    title:str
    author: Optional[str] = None
    description:Optional[str] = None
class WorkCreate(WorkBase):
    pass
class WorkOut(WorkBase):
    id: int
    file_path: Optional[str]
    created_at: datetime

    class Config:
        orm_mode = True
class ChapterOut(BaseModel):
    id: int
    work_id: int
    chapter_num: int
    title: Optional[str]
    text: str

    class Config:
        orm_mode = True

class AskRequest(BaseModel):
    question: str
