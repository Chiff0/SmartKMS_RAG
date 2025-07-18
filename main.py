import logging
import uvicorn
from dotenv import load_dotenv
from contextlib import asynccontextmanager
from fastapi import FastAPI
from mangum import Mangum


from api.endpoints import router as api_router
from core.rag_services import initialize_rag_chain


load_dotenv()

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)


@asynccontextmanager
async def lifespan(app_instance: FastAPI):
    logger.info("Initializing RAG chain...")
    initialize_rag_chain()
    logger.info("complete.")
    yield
    logger.info("Shutting down...")


app = FastAPI(
    title="Modular RAG Agent",
    description="burek",
    version="4.0.0",
    lifespan=lifespan
)

app.include_router(api_router, prefix="/api/v1")

# --- AWS Lambda Handler ---
handler = Mangum(app)

# --- Local Development Runner ---
if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000, log_level="info")