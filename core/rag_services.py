import os
import logging
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from langchain_core.runnables import RunnablePassthrough
from langchain_core.output_parsers import StrOutputParser

# Import the query function from the standalone service directory
from kms_db_service.db_service import query

logger = logging.getLogger(__name__)

# The RAG chain will now live in this service layer
rag_chain = None

def initialize_rag_chain():
    """Initializes the LangChain components for RAG."""
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

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {"context": lambda x: format_docs(query(x["question"])), "question": RunnablePassthrough()}
        | prompt
        | llm
        | StrOutputParser()
    )
    logger.info("RAG chain with OpenAI LLM initialized.")


def get_streaming_response(question: str):
    """Handles the logic for a streaming query."""
    if not rag_chain:
        raise ConnectionError("RAG chain is not initialized.")
    return rag_chain.stream({"question": question})


def get_non_streaming_response(question: str):
    """Handles the logic for a non-streaming query."""
    if not rag_chain:
        raise ConnectionError("RAG chain is not initialized.")
    
    # Retrieve source documents first
    source_documents = query(question)
    # Invoke the chain to get the generated answer
    answer = rag_chain.invoke({"question": question})

    sources = [
        {
            "page_content": doc.page_content,
            "metadata": doc.metadata,
        } for doc in source_documents
    ]
    
    return {"answer": answer, "sources": sources}

def is_rag_ready():
    """Health check for the RAG service."""
    return rag_chain is not None