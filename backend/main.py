# 1. Import the required tools
import logging
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from .database import create_tables, get_connection
from .routes import router

# 2. Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

request_counts = {}
response_times = {}

# 3. Create the FastAPI application
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
        f"{response.status_code} - {elapsed_time:.4f} seconds"
    )

    if response.status_code >= 400:
        logger.warning(log_message)
    else:
        logger.info(log_message)

    return response


# 4. Configure communication with the frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=False,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 5. Prepare the database
create_tables()

# 6. Log successful startup
logger.info("AeroOps started successfully")

# 7. Include the API routes
app.include_router(router)


# 8. Define the root route
@app.get("/")
def read_root():
    return {"message": "AeroOps API is running"}


# 9. Define the API health route
@app.get("/health")
def health_check():
    return {"status": "ok"}


# 10. Define the database health route
@app.get("/health/database")
def database_health_check():
    connection = get_connection()
    connection.execute("SELECT 1")
    connection.close()

    return {
        "status": "ok",
        "database": "connected",
    }