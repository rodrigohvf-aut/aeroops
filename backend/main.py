# 1. Importar as ferramentas necessárias
import logging

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables, get_connection
from .routes import router


# 2. Configurar os logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# 3. Criar a aplicação FastAPI
app = FastAPI(title="AeroOps")


# 4. Configurar a comunicação com o front-end
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)


# 5. Preparar o banco de dados
create_tables()


# 6. Registrar que a aplicação foi iniciada
logger.info("AeroOps iniciado com sucesso")


# 7. Conectar as rotas à aplicação
app.include_router(router)


# 8. Definir a rota principal
@app.get("/")
def read_root():
    return {"message": "AeroOps API funcionando"}


# 9. Definir a rota de saúde da API
@app.get("/health")
def health_check():
    return {"status": "ok"}


# 10. Definir a rota de saúde do banco
@app.get("/health/database")
def database_health_check():
    connection = get_connection()
    connection.execute("SELECT 1")
    connection.close()

    return {
        "status": "ok",
        "database": "connected",
    }