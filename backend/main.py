from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import create_tables
from .routes import router
app = FastAPI(title="AeroOps")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

create_tables()
app.include_router(router)

@app.get("/")
def read_root():
    return {"message": "AeroOps API funcionando"}

@app.get("/health")
def health_check():
    return {"status": "ok"}