from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# 1. SQLite Database file ka naam aur path set karna
import os
# Purani line ko hata kar ye likhein:
SQLALCHEMY_DATABASE_URL = "sqlite:///" + os.path.join(os.path.abspath(os.path.dirname(__file__)), "students.db")

# 2. Database engine create karna
engine = create_engine(
    SQLALCHEMY_DATABASE_URL, connect_args={"check_same_thread": False}
)

# 3. Database session banane ke liye sessionmaker setup karna
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 4. Models ke liye Base class create karna
Base = declarative_base()

# 5. Dependency: Jo har request ke liye DB session open aur close karegi
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()