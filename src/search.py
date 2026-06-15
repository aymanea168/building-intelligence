"""
Search and RAG pipeline for construction defect detection.

Provides:
- Text and image similarity search
- Context building from retrieval results
- LLM-based report generation using RAG
"""

from typing import Any, Dict, Optional

import torch
from PIL import Image

from .models import (
    MODEL,
    chroma_client,
    clip_model,
    device,
    llm_client,
    preprocess,
    text_model,
)

# ============================================================================
# Collection References
# ============================================================================

text_collection = chroma_client.get_collection("construction_defects_text")
image_collection = chroma_client.get_collection("construction_defects_image")


# ============================================================================
# Search Functions
# ============================================================================


def search_text(query: str, k: int = 5) -> Dict[str, Any]:
    """
    Search for similar defects using text query.

    Args:
        query: Text query describing the defect
        k: Number of results to return

    Returns:
        Query results with documents, metadatas, distances
    """
    emb = text_model.encode(query).tolist()
    return text_collection.query(query_embeddings=[emb], n_results=k) # type: ignore


def search_image(path: str, k: int = 5) -> Dict[str, Any]:
    """
    Search for similar defects using image query.

    Args:
        path: Path to the image file
        k: Number of results to return

    Returns:
        Query results with documents, metadatas, distances
    """
    img = preprocess(Image.open(path).convert("RGB")).unsqueeze(0).to(device)
    with torch.no_grad():
        emb = clip_model.encode_image(img).cpu().numpy()[0].tolist() # type: ignore

    return image_collection.query(query_embeddings=[emb], n_results=k) # type: ignore


# ============================================================================
# Context Building
# ============================================================================


def build_context(search_results: Dict[str, Any]) -> str:
    """
    Build a formatted context string from search results.

    Args:
        search_results: Results from ChromaDB query

    Returns:
        Formatted context string with defect details
    """
    docs = search_results["documents"][0]
    metas = search_results["metadatas"][0]

    context_parts = []
    for doc, metadata in zip(docs, metas):
        context_parts.append(
            f"""
            Defect: {metadata.get('defect', '')}
            Image: {metadata.get('image_path', '')}
            Details of the defect: {doc}
            """
        )
    return "\n---\n".join(context_parts)


# ============================================================================
# Report Generation
# ============================================================================


def generate_report(context: str, user_input: Optional[str] = None) -> str:
    """
    Generate an expert report using LLM with retrieved context.

    Args:
        context: Retrieved context from search results
        user_input: User's query or observation

    Returns:
        Expert analysis report
    """
    prompt = f"""
You are a construction inspection expert (SECO-style).

Use retrieved cases below:

{context}

User input:
{user_input}

Return:
- defect interpretation
- severity
- possible causes
- inspection plan
- recommendations

Be technical and concise.
"""

    response = llm_client.chat.completions.create(
        model=MODEL,
        messages=[{"role": "user", "content": prompt}],
    )

    return  str(response.choices[0].message.content)


# ============================================================================
# RAG Pipeline
# ============================================================================


def rag_pipeline(
    query: Optional[str] = None,
    image_path: Optional[str] = None,
) -> str:
    """
    Execute the complete RAG pipeline: search → context building → report.

    Args:
        query: Text query for defect search
        image_path: Path to image for defect search

    Returns:
        Generated expert report
    """
    context_parts = []

    if image_path:
        results = search_image(image_path)
        context_parts.append("from image query: " + build_context(results))

    if query:
        results = search_text(query)
        context_parts.append("from text query: " + build_context(results))

    context = "\n".join(context_parts)
    return generate_report(context, query)


