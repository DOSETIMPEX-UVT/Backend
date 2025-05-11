from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import engine, Base
from app.routers import users
from app.routers import conversations
from app.routers import messages
from app.routers import vector_response

app = FastAPI()

# Adăugăm CORS ca să putem comunica cu frontend-ul
origins = [
    "http://localhost:5173",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Creează automat toate tabelele
@app.on_event("startup")
def on_startup():
    print("Verific tabelele în baza de date...")
    Base.metadata.create_all(bind=engine)
    print("Tabele verificate/creat!")

# Include rutele
app.include_router(users.router)
app.include_router(conversations.router)
app.include_router(messages.router)
app.include_router(vector_response.router)