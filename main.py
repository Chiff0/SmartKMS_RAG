import logging
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum

# Import from your new structured files
from api.endpoints import router as api_router
from core.rag_services import initialize_rag_chain
from core.ingestion import ingest_documents_on_startup

load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    """Handles application startup logic."""
    logger.info("Application startup: Initializing services...")
    initialize_rag_chain()
    ingest_documents_on_startup()
    logger.info("Application startup complete.")
    yield
    logger.info("Application shutdown.")

app = FastAPI(
    title="Modular RAG Agent",
    description="A RAG agent with a modular structure for services, endpoints, and models.",
    version="4.0.0",
    lifespan=lifespan
)

# Include the API router. It's good practice to add a prefix.
app.include_router(api_router, prefix="/api/v1")

# --- AWS Lambda Handler ---
handler = Mangum(app)

# --- Local Development Runner ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")