import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# Get the absolute path to the directory containing this file
BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# Go up one level (if this file is in 'app/') to locate jobs.db at root
PROJECT_ROOT = os.path.dirname(BASE_DIR)
DEFAULT_DB_PATH = f"sqlite:///{os.path.join(PROJECT_ROOT, 'jobs.db')}"

DATABASE_URL = os.getenv("DATABASE_URL", DEFAULT_DB_PATH)

if DATABASE_URL.startswith("postgres://"):
    DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://", 1)

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {}
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()