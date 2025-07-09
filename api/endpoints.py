import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

# Import the models and services
from models.request_models import QueryRequest
from core import rag_services

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/query/stream", summary="Query the RAG agent and stream the response")
async def query_stream_endpoint(request: QueryRequest):
    logger.info(f"Streaming query received: '{request.query[:70]}...'")
    try:
        response_stream = rag_services.get_streaming_response(request.query)
        return StreamingResponse(response_stream, media_type="text/plain")
    except ConnectionError as e:
        logger.error(f"Service not ready error during streaming query: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error during streaming query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing streaming query.")

@router.post("/query/non-stream", summary="Query the RAG agent and get a full response")
async def query_non_stream_endpoint(request: QueryRequest):
    logger.info(f"Non-streaming query received: '{request.query[:70]}...'")
    try:
        response = rag_services.get_non_streaming_response(request.query)
        return response
    except ConnectionError as e:
        logger.error(f"Service not ready error during non-streaming query: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error during non-streaming query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing non-streaming query.")

@router.get("/health", summary="Health check endpoint")
async def health_check():
    if rag_services.is_rag_ready():
        return {"status": "healthy", "message": "RAG components initialized."}
    else:
        return {"status": "degraded", "message": "RAG components not initialized."}