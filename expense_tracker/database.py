import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from .models import Base

# Database lives in the current folder by default; tests (or users) can
# point elsewhere with the EXPENSE_TRACKER_DB environment variable.
DATABASE_URL = os.environ.get("EXPENSE_TRACKER_DB", "sqlite:///expenses.db")

engine = create_engine(DATABASE_URL, echo=False)
SessionLocal = sessionmaker(bind=engine)

def init_db():
    Base.metadata.create_all(bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()