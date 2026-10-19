# 1. Importar as ferramentas necessárias
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables, get_connection
from .routes import router

# 2. Configurar os logs
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

request_counts = {}
response_times = {}

# 3. Criar a aplicação FastAPI
app = FastAPI(title="AeroOps")

@app.middleware("http")
async def log_response_time(request, call_next):
    start_time = time.perf_counter()

    response = await call_next(request)

    elapsed_time = time.perf_counter() - start_time
    
    request_key = f"{request.method} {request.url.path}"
    request_counts[request_key] = request_counts.get(request_key, 0) + 1    
    response_times.setdefault(request_key, []).append(elapsed_time)

    log_message = (
    f"{request.method} {request.url.path} - "
    f"{response.status_code} - {elapsed_time:.4f} segundos"
    )

    if response.status_code >= 400:
        logger.warning(log_message)
    else:
        logger.info(log_message)

    return response

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