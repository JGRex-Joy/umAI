from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

db_url = 'sqlite:///fastapi-test.db'
engine = create_engine(db_url)
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)
