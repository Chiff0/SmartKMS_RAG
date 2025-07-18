import logging
from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse
from typing import Optional

from models.request_models import QueryRequest
from models.request_models import QueryRequest, PushRequest
from core import rag_services

logger = logging.getLogger(__name__)
router = APIRouter()

@router.post("/query/stream", summary="Query the RAG agent and stream the response")
async def query_stream_endpoint(request: QueryRequest):
    logger.info(f"Streaming query received for user '{request.user}'")
    try:
        response_stream = await rag_services.get_streaming_response(
            question=request.query,
            user=request.user,
            req_type=request.type,
            req_source=request.source
        )
        return StreamingResponse(response_stream, media_type="text/plain")
    except ConnectionError as e:
        logger.error(f"Service not ready error during streaming query: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error during streaming query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing streaming query.")

@router.post("/query/non-stream", summary="Query the RAG agent and get a full response")
async def query_non_stream_endpoint(request: QueryRequest):
    logger.info(f"Non-streaming query received for user '{request.user}'")
    try:
        response = await rag_services.get_non_streaming_response(
            question=request.query,
            user=request.user,
            req_type=request.type,
            req_source=request.source
        )
        return response
    except ConnectionError as e:
        logger.error(f"Service not ready error during non-streaming query: {e}")
        raise HTTPException(status_code=503, detail=str(e))
    except Exception as e:
        logger.error(f"Error during non-streaming query: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Error processing non-streaming query.")

@router.post("/push", summary="Push new data for ingestion")
async def push_data_endpoint(request: PushRequest):
    logger.info(f"Push request received for platform '{request.platform}' with id '{request.id}'")
    try:
        response = await rag_services.push_data_to_api(request.dict())
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing push request: {e}")

@router.get("/query", summary="Proxy for the GET /KM/query endpoint")
async def get_query_endpoint(
    user: str,
    type: Optional[str] = None,
    source: Optional[str] = None
):
    logger.info(f"GET query request received for user '{user}'")
    try:
        response = await rag_services.get_data_from_query_api(
            user=user,
            req_type=type,
            req_source=source
        )
        return response
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing GET query request: {e}")



@router.get("/health", summary="Health check endpoint")
async def health_check():
    if rag_services.is_rag_ready():
        return {"status": "healthy", "message": "RAG components initialized."}
    else:
        return {"status": "degraded", "message": "RAG components not initialized."}