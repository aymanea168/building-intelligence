"""
Model initialization and configuration for construction defect detection.

Includes:
- LLM client (OpenRouter API)
- Vector database (ChromaDB)
- Text embeddings (Sentence Transformers)
- Image embeddings (OpenCLIP)
"""

import os
from typing import Callable

import chromadb
import open_clip
import torch
from dotenv import load_dotenv
from openai import OpenAI
from sentence_transformers import SentenceTransformer
from torchvision.transforms import Compose

# Load environment variables
load_dotenv(".env")

# ============================================================================
# LLM Configuration
# ============================================================================

OPENROUTER_API_KEY = os.getenv("OPENROUTER_API_KEY")
MODEL = os.getenv("MODEL", "openai/gpt-oss-120b:free")

llm_client = OpenAI(
    base_url="https://openrouter.ai/api/v1",
    api_key=OPENROUTER_API_KEY,
)

# ============================================================================
# Vector Database Configuration
# ============================================================================

chroma_client = chromadb.PersistentClient(path="db/")

text_collection = chroma_client.get_or_create_collection(
    name="construction_defects_text"
)

image_collection = chroma_client.get_or_create_collection(
    name="construction_defects_image"
)

# ============================================================================
# Embedding Models
# ============================================================================

# Text embedding model
text_model = SentenceTransformer("all-MiniLM-L6-v2")

# Image embedding model (OpenCLIP ViT-B-32)
clip_model, _, preprocess_fn = open_clip.create_model_and_transforms(
    "ViT-B-32",
    pretrained="openai",
)

preprocess: Callable = preprocess_fn # type: ignore

# ============================================================================
# Device Configuration
# ============================================================================

device = "cuda" if torch.cuda.is_available() else "cpu"
