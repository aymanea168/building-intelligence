"""
Embedding pipeline for construction defects.

Processes enriched dataset to create vector embeddings:
- Text embeddings using Sentence Transformers (384D)
- Image embeddings using OpenCLIP (512D)
- Stores embeddings in ChromaDB collections
"""

import json
from typing import Any, Dict

import torch
from PIL import Image

from models import (
    clip_model,
    device,
    image_collection,
    preprocess,
    text_collection,
    text_model,
)


# ============================================================================
# Helper Functions
# ============================================================================


def create_document(item: Dict[str, Any]) -> str:
    """
    Create formatted document from defect item.

    Args:
        item: Defect data dictionary

    Returns:
        Formatted document string
    """
    document = f"""
Defect type: {item['defect']}
Description: {item['description']}
Severity: {item['severity']}
Causes: {', '.join(item['causes'])}
Inspection actions: {', '.join(item['inspection_actions'])}
Recommendations: {', '.join(item['recommendations'])}
"""
    return document


# ============================================================================
# Model Setup
# ============================================================================

clip_model.eval()
clip_model.to(device)


# ============================================================================
# Embedding Pipeline
# ============================================================================


def embed_dataset(data_path: str = "data/enriched_openrouter.json") -> None:
    """
    Process dataset and create embeddings for text and images.

    Args:
        data_path: Path to the enriched dataset JSON file
    """
    with open(data_path) as f:
        data = json.load(f)

    for idx, item in enumerate(data):
        doc_id = str(idx)

        # ====================================================================
        # Text Embedding (384D)
        # ====================================================================

        document = create_document(item)
        text_vector = text_model.encode(document).tolist()

        text_collection.add(
            ids=[f"text_{doc_id}"],
            documents=[document],
            embeddings=[text_vector],
            metadatas=[
                {
                    "image_path": item["image_path"],
                    "defect": item["defect"],
                }
            ],
        )

        # ====================================================================
        # Image Embedding (512D)
        # ====================================================================

        image = Image.open(item["image_path"]).convert("RGB")
        image_tensor = preprocess(image).unsqueeze(0).to(device)

    with torch.no_grad():
        image_vector = clip_model.encode_image(image_tensor).cpu().numpy()[0].tolist() # type: ignore

        image_collection.add(
            ids=[f"img_{doc_id}"],
            documents=[document],  # Optional but useful for debugging
            embeddings=[image_vector],
            metadatas=[
                {
                    "image_path": item["image_path"],
                    "defect": item["defect"],
                }
            ],
        )


if __name__ == "__main__":
    embed_dataset()
    print("Database created successfully")
