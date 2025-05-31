# database.py
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

# --- TEMPORARY DEBUGGING/FIXING LINE START ---
# Construct the absolute path to your .env file
# Ensure this path is EXACTLY correct for your system
# Replace 'back-end' with 'back_end' if your folder name uses underscore
dotenv_path_absolute = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.env')
print(f"DEBUG: Attempting to load .env from: {dotenv_path_absolute}")
load_dotenv(dotenv_path=dotenv_path_absolute)
# --- TEMPORARY DEBUGGING/FIXING LINE END ---


SQLALCHEMY_DATABASE_URL = os.getenv("DATABASE_URL")

print(f"DEBUG: Value of DATABASE_URL from os.getenv() AFTER forced load: {SQLALCHEMY_DATABASE_URL}")

if not SQLALCHEMY_DATABASE_URL:
    raise ValueError("DATABASE_URL environment variable not set.")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()