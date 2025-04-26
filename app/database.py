from sqlalchemy import create_engine #creaza o conexiune intre app(app) si baza de date PostgreSQL
from sqlalchemy.orm import sessionmaker, declarative_base  #permite crearea de sesiuni de lucru cu baza (operatii de adaugare, modificare etc)

DATABASE_URL = "postgresql://username:password@localhost:5432/DataBaseName"

engine = create_engine(DATABASE_URL)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db  # oferă sesiunea către route
    finally:
        db.close()  # când ruta se termină, închide conexiunea
