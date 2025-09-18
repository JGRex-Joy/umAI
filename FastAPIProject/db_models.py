
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import declarative_base, relationship

Base = declarative_base()

class Work(Base):
    __tablename__ = "works"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    author = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    file_path = Column(String, nullable=True)  # хранение пути к загруженному PDF
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    chapters = relationship("Chapter", back_populates="work", cascade="all, delete-orphan")


class Chapter(Base):
    __tablename__ = "chapters"

    id = Column(Integer, primary_key=True, index=True)
    work_id = Column(Integer, ForeignKey("works.id"), nullable=False)
    chapter_num = Column(Integer, nullable=False)
    title = Column(String, nullable=True)
    text = Column(Text, nullable=False)
    work = relationship("Work", back_populates="chapters")





