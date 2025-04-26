from fastapi import FastAPI
from app.database import engine, Base
from app.routers import users
from app.routers import conversations
from app.routers import messages
app = FastAPI()

# Creează automat toate tabelele dacă nu există
@app.on_event("startup")
def on_startup():
    print("Verific tabelele în baza de date...")
    Base.metadata.create_all(bind=engine)
    print("Tabele verificate/creat!")

# Include rutele
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)