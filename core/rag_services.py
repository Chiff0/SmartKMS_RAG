import os
import httpx
import logging
from typing import Optional
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

logger = logging.getLogger(__name__)
QUERY_API_URL = os.getenv("QUERY_API_URL", "http://127.0.0.1:8100/KM/search")
DATA_API_URL = os.getenv("DATA_API_URL", "http://localhost:8000/KM/push")
GET_QUERY_API_URL = os.getenv("GET_QUERY_API_URL", "http://localhost:8100/KM/query")
rag_chain = None

async def get_context_from_api(question: str, user: str, req_type: Optional[str], req_source: Optional[str]) -> str:
    if not QUERY_API_URL:
        logger.error("QUERY_API_URL environment variable is not set.")
        raise ValueError("QUERY_API_URL is not configured.")

    request_body = {
        "context": question,
        "user": user,
        "type": req_type,
        "source": req_source
    }
    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                QUERY_API_URL,
                json=request_body,
                timeout=15.0
            )
            response.raise_for_status()
            data = response.json()
            sources = data.get("sources", [])
            if not sources:
                return "No relevant context was found in the database."
            return "\n\n".join(doc.get("page_content", "") for doc in sources)
    except httpx.RequestError as e:
        logger.error(f"HTTP request to Query API failed: {e}")
        return "Error: Could not retrieve context from the database service."

async def push_data_to_api(push_data: dict) -> dict:
    if not DATA_API_URL:
        logger.error("DATA_API_URL environment variable is not set.")
        raise ValueError("DATA_API_URL is not configured.")

    try:
        async with httpx.AsyncClient() as client:
            response = await client.post(
                DATA_API_URL,
                json=push_data,
                timeout=30.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"HTTP request to Data API failed: {e}")
        raise

async def get_data_from_query_api(user: str, req_type: Optional[str], req_source: Optional[str]) -> dict:
    if not GET_QUERY_API_URL:
        logger.error("GET_QUERY_API_URL environment variable is not set.")
        raise ValueError("GET_QUERY_API_URL is not configured.")

    params = {"user": user}
    if req_type:
        params["type"] = req_type
    if req_source:
        params["source"] = req_source

    try:
        async with httpx.AsyncClient() as client:
            response = await client.get(
                GET_QUERY_API_URL,
                params=params,
                timeout=15.0
            )
            response.raise_for_status()
            return response.json()
    except httpx.RequestError as e:
        logger.error(f"HTTP request to GET Query API failed: {e}")
        raise

def initialize_rag_chain():
    global rag_chain
    llm = ChatOpenAI(
        model=os.getenv("OPENAI_MODEL_NAME", "gpt-4o"), 
        temperature=0, 
        streaming=True
    )
    prompt_template = """
    Answer the question based only on the following context:

    Context:
    {context}

    Question:
    {question}
    """
    prompt = ChatPromptTemplate.from_template(prompt_template)
    rag_chain = (
        {"context": lambda x: get_context_from_api(x["question"], x["user"], x["type"], x["source"]), 
         "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain initialized to use remote Query API.")

async def get_streaming_response(question: str, user: str, req_type: Optional[str], req_source: Optional[str]):
    if not rag_chain:
        raise ConnectionError("RAG chain is not initialized.")
    return rag_chain.astream({"question": question, "user": user, "type": req_type, "source": req_source})

async def get_non_streaming_response(question: str, user: str, req_type: Optional[str], req_source: Optional[str]):
    if not rag_chain:
        raise ConnectionError("RAG chain is not initialized.")
    
    answer = await rag_chain.ainvoke({"question": question, "user": user, "type": req_type, "source": req_source})
    
    # TODO make sure sources work
    return {"answer": answer, "sources": []}

def is_rag_ready():
    return rag_chain is not None