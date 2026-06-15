"""
FastAPI application for construction defect analysis.

Provides endpoints for:
- Document uploads
- RAG-based defect analysis via text and/or image
"""

import os
import shutil
from typing import Optional

from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from .search import generate_report, rag_pipeline


# ============================================================================
# Configuration
# ============================================================================

UPLOAD_DIR = "media"
ALLOWED_ORIGINS = [
    "http://localhost:5173",  # Frontend dev server
    "http://localhost:3000",  # Alternative frontend
]

os.makedirs(UPLOAD_DIR, exist_ok=True)


# ============================================================================
# FastAPI Setup
# ============================================================================

app = FastAPI(
    title="Construction Defect Analysis API",
    description="RAG-based defect detection and analysis system",
    version="1.0.0",
)

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


# ============================================================================
# Request/Response Models
# ============================================================================


class ChatRequest(BaseModel):
    """User query with optional image for analysis."""

    prompt: str
    img_path: Optional[str] = None


class ChatResponse(BaseModel):
    """Generated analysis report."""

    text: str


# ============================================================================
# Endpoints
# ============================================================================


@app.get("/")
def health_check() -> dict:
    """Health check endpoint."""
    return {"status": "ok", "service": "construction-defect-analysis"}


@app.post("/upload-only")
def upload_only(file: UploadFile = File(...)) -> dict:
    """
    Upload a file to the server.

    Args:
        file: Image file to upload

    Returns:
        Dictionary with saved file path
    """
    file_path = os.path.join(UPLOAD_DIR, file.filename) # type: ignore

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    return {"path": file_path}


@app.post("/api/chat", response_model=ChatResponse)
def chat(request: ChatRequest) -> ChatResponse:
    """
    Analyze defects using text query and/or image.

    Args:
        request: ChatRequest with prompt and optional image path

    Returns:
        ChatResponse with analysis report
    """
    analysis = rag_pipeline(
        query=request.prompt,
        image_path=request.img_path,
    )

    return ChatResponse(text=analysis)
