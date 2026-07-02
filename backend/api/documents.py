"""Document upload and ingestion API."""

import logging
import shutil
from pathlib import Path

from fastapi import APIRouter, File, HTTPException, UploadFile

from backend.rag.ingest import ingest_directory, ingest_file

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/documents", tags=["documents"])

DOCUMENTS_DIR = Path("/app/documents")
ALLOWED_EXTENSIONS = {".md", ".txt"}


@router.post("/upload")
async def upload_document(file: UploadFile = File(...)):
    """Upload and ingest a bank document into the knowledge base."""
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required.")

    suffix = Path(file.filename).suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=(
                f"Unsupported file type '{suffix}'. "
                "Only Markdown (.md) and plain text (.txt) policy documents can be added. "
                "Images and PDFs are not supported in this demo."
            ),
        )

    DOCUMENTS_DIR.mkdir(parents=True, exist_ok=True)
    dest = DOCUMENTS_DIR / Path(file.filename).name
    with dest.open("wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    chunks = ingest_file(dest, force=True)
    if chunks == 0:
        raise HTTPException(
            status_code=400,
            detail=(
                f"'{file.filename}' was saved but contains no readable text to index. "
                "Use a .md or .txt file with policy content."
            ),
        )

    return {
        "filename": dest.name,
        "chunks_ingested": chunks,
        "status": "success",
        "message": (
            f"Document '{dest.name}' was added to the knowledge base "
            f"({chunks} searchable sections)."
        ),
    }


@router.post("/ingest-all")
async def ingest_all_documents():
    """Re-ingest all documents from the documents directory."""
    results = ingest_directory(DOCUMENTS_DIR)
    return {"ingested": results, "total_chunks": sum(results.values())}


@router.get("/tools")
async def list_mcp_tools():
    """Return MCP-compatible tool manifest."""
    from backend.tools.registry import tools_as_mcp_manifest

    return tools_as_mcp_manifest()
