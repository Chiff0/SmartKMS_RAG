import os
import logging

from kms_db_service.db_service import store_pdf_files, store_msoffice_files

logger = logging.getLogger(__name__)
DOC_DIR = os.getenv("DOC_DIR", "data")

def ingest_documents_on_startup():
    if not os.path.exists(DOC_DIR):
        logger.warning(f"Data directory '{DOC_DIR}' not found. Skipping ingestion.")
        os.makedirs(DOC_DIR)
        logger.info(f"Created data directory at '{DOC_DIR}'. Place files here for ingestion on next startup.")
        return

    logger.info(f"Scanning '{DOC_DIR}' for documents to ingest...")
    try:
        files_to_ingest = [f for f in os.listdir(DOC_DIR) if os.path.isfile(os.path.join(DOC_DIR, f))]
    except OSError as e:
        logger.error(f"Could not scan directory '{DOC_DIR}': {e}")
        return
    
    if not files_to_ingest:
        logger.info("No documents found in the data directory to ingest.")
        return

    for filename in files_to_ingest:
        filepath = os.path.join(DOC_DIR, filename)
        file_extension = os.path.splitext(filename)[1].lower()
        metadata = {"source_file": filename}
        
        try:
            with open(filepath, "rb") as f:
                logger.info(f"Ingesting '{filename}'...")
                if file_extension == ".pdf":
                    store_pdf_files(f, metadata)
                elif file_extension in [".docx", ".xlsx", ".pptx"]:
                    store_msoffice_files(f, metadata)
                else:
                    logger.warning(f"Skipping unsupported file type: {filename}")
        except Exception as e:
            logger.error(f"Failed to ingest '{filename}': {e}", exc_info=True)