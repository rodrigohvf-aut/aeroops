from fastapi import FastAPI
from .routes import router
from .database import create_tables
app = FastAPI(title="AeroOps")
create_tables()
app.include_router(router)


@app.get("/")
def read_root():
    return {"message": "AeroOps API funcionando"}


@app.get("/health")
def health_check():
    return {"status": "ok"}