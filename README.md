# Building Intelligence: AI-Powered Construction Defect Analysis

**A retrieval-augmented generation (RAG) system for construction defect detection, and expert analysis.**

---

## Table of Contents

1. [Overview](#overview)
2. [Problem & Target Audience](#problem--target-audience)
3. [Relevance to SECO](#relevance-to-seco)
4. [Key Features](#key-features)
5. [Data Sources](#data-sources)
6. [Architecture](#architecture)
7. [Technical Decisions & Trade-offs](#technical-decisions--trade-offs)
8. [Project Structure](#project-structure)
9. [Setup & Installation](#setup--installation)
10. [Usage](#usage)
11. [API Endpoints](#api-endpoints)
12. [What's Production-Ready vs. What Would Be Discarded](#whats-production-ready-vs-what-would-be-discarded)
13. [3-Month Roadmap](#3-month-roadmap)
14. [Contributing](#contributing)

---

## Overview

Building Intelligence is an AI system that analyzes construction defect images and text descriptions to provide expert-level inspection reports. It combines:

- **Multimodal embeddings** (text + image) for similarity search
- **Vision Language Models (VLMs)** for intelligent analysis and text enrichment of the images
- **Retrieval-Augmented Generation (RAG)** to find similar defects in a knowledge base
- **ChromaDB** for scalable vector storage

When a construction inspector photographs a defect or describes it (with an initial observation), the system retrieves similar historical cases and generates a professional report including:
- Defect interpretation
- Severity classification (low/medium/high)
- Root cause analysis
- Inspection actions
- Recommendations

---

## Problem & Target Audience

### The Problem

Construction inspectors and quality assurance teams face several challenges:

1. **Knowledge consistency**: Defect interpretation varies across inspectors due to experience differences
2. **Documentation burden**: Writing detailed inspection reports is time-consuming and repetitive
3. **Precedent unavailability**: Inspectors lack instant access to similar past cases for reference
4. **Decision support**: Complex defects require expert consultation, creating bottlenecks
5. **Scalability**: Manual inspection processes don't scale with project size

### Target Audience

- **Construction inspectors** who need quick, consistent defect analysis
- **Quality assurance managers** who oversee inspection reports and documentation
- **Project engineers** who need historical defect analysis for decision-making
- **Construction companies** seeking to standardize inspection protocols

---

## Relevance to SECO

SECO, in this case, can leverage this Building Intelligence AI tool to:

1. **Standardize quality control** across multiple projects and teams
2. **Reduce inspection time** by automating report generation (time savings expected within seconds)
3. **Improve consistency** by basing decisions on historical data, not individual experience
4. **Build institutional knowledge** by accumulating defect cases into a searchable database
5. **Competitive advantage** through faster, more thorough inspections at lower cost
6. **Risk mitigation** by ensuring no defect classification is missed or underestimated

The system aligns with SECO as a service provider and **data-driven inspection authority** with quantifiable quality.

---

## Key Features

**Multimodal Search**: Query by image, text, or both  
**VLM Enrichment**: Automated dataset labeling using vision language models  
**RAG Pipeline**: Retrieves similar historical cases before generating reports  
**RESTful API**: Easy integration with mobile apps or web dashboards

---

## Data Sources

### Primary: MBDD2025 (Multi-Building Defect Dataset from Kaggle)

**Why MBDD2025?**

- **Comprehensive**: 10,000+ labeled construction defect images
- **Diverse**: Covers 5 major defect classes: cracks, leakage, corrosion, abscission (spalling), bulge
- **Real-world**: Authentic building images from Chinese multi-dwelling buildings
- **Structured labels**: YOLO format (.txt files) for easy parsing
- **Balanced**: Stratified sampling ensures equal representation across classes

**Dataset Structure**:
```
data/raw/MBDD2025/
├── images/          # 10,000+ .jpg files
└── labels/          # Corresponding .txt files
```

**Classes**:
- `0: crack` – Surface fractures, hairline to structural cracks
- `1: leakage` – Water infiltration, stains, seepage
- `2: corrosion` – Rust, efflorescence, material degradation
- `3: abscission` – Surface spalling, concrete breakaway, delamination
- `4: bulge` – Swelling, distortion, deformation

### Secondary: Enrichment via VLM

The dataset is enriched using OpenRouter API with VLMs (Vision Language Models) to generate:
- Detailed technical descriptions
- Severity classifications
- Root cause hypotheses
- Inspection actions
- Recommendations

This creates a **synthetic expert annotation layer** that improves RAG retrieval quality.

---

## Architecture

### System Flow

```
┌──────────────────────┐
│  User Input          │
│  (Text + Image)      │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────────────┐
│  Embedding Generation        │
│  • Text: SentenceTransformer │
│  • Image: OpenCLIP (ViT-B)   │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Similarity Search (ChromaDB)│
│  • Retrieve k=5 similar cases│
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  Context Aggregation         │
│  • Combine retrieved docs    │
│  • Format for LLM prompt     │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  LLM Analysis (OpenRouter)   │
│  • GPT-oss-120b (free tier)  │
│  • Professional report gen.  │
└──────────┬───────────────────┘
           │
           ▼
┌──────────────────────────────┐
│  API Response                │
│  (JSON with analysis report) │
└──────────────────────────────┘
```

### Technology Stack

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| **Embeddings (Text)** | Sentence-Transformers (all-MiniLM-L6-v2) | 384D, fast, requires no GPU |
| **Embeddings (Image)** | OpenCLIP (ViT-B-32) | 512D, multimodal alignment with text, free weights |
| **Vector DB** | ChromaDB | Lightweight, persistent, supports metadata filtering |
| **LLM** | OpenRouter (GPT-oss-120b) | Free tier, good quality, no API key cost |
| **Backend** | FastAPI | Async, modern, minimal overhead |
| **Frontend** | React + Vite | Future-proof, component-based, HMR support |
| **Compute** | CPU + optional GPU | Embeddings run on CPU; inference on GPU if available |

---

## Technical Decisions & Trade-offs

### Decision 1: Two-Tower Embedding Architecture

**Decision**: Maintain separate text and image embeddings (384D + 512D) rather than a unified multimodal space.

**Rationale**:
- Text model is faster and more space-efficient
- Image model captures visual features better
- Allows independent optimization

**Trade-off**: Requires dual searches; slightly higher latency (~100ms overhead).


---

### Decision 2: VLM Enrichment Over Manual Labeling

**Decision**: Use OpenRouter VLM API to auto-generate severity, causes, and recommendations instead of hiring domain experts.

**Rationale**:
- Faster bootstrapping (hours vs. weeks)
- Consistent structured output
- Scalable to new data
- Cost-effective (OpenRouter free tier)

**Trade-off**: Quality depends on model hallucinations; although it requires human review in production; may miss industry-specific nuances.

---

### Decision 3: RAG Over Fine-Tuned Models

**Decision**: Use retrieval-augmented generation (RAG) instead of fine-tuning a task-specific model.

**Rationale**:
- No GPU required for training
- Updates to knowledge base don't require retraining
- Explainability: users see which cases informed the decision
- Lower cost and faster iteration

**Trade-off**: Latency is higher (compared with a tuned model); quality depends on retrieval quality.

---

### Decision 4: ChromaDB Over Traditional Vector Databases

**Decision**: Use ChromaDB for vector storage.

**Rationale**:
- Fully local deployment (no cloud dependency)
- Persistent storage (SQLite) without additional infrastructure
- Metadata filtering on defect class and image path
- Simple API, easy to debug

**Trade-off**: Not designed for distributed systems; struggles large datasets, but fits what is needed for this particular project; limited production monitoring.


---

## Project Structure

```
building-intelligence/
├── README.md                           # This file
├── requirements.txt                    # Python dependencies
│
├── src/
│   ├── main.py                        # FastAPI application
│   ├── models.py                      # Model initialization (embeddings, LLM, ChromaDB)
│   ├── search.py                      # RAG pipeline & similarity search
│   ├── embeddings.py                  # Embedding generation and storage
│   ├── data_enrichment.py             # VLM-based dataset enrichment
│   ├── build_dataset.py               # Dataset building from raw sources
│   └── scripts/
│       └── scrape.py                  # MBDD2025 parser with stratified sampling
│
├── frontend/                          # React + Vite frontend
│   ├── package.json
│   ├── index.html
│   └── src/
│
├── data/
│   ├── processed/
│   │   └── metadata.csv              # Dataset metadata (image_path, defect, dataset)
│   │
│   ├── enriched_openrouter.json      # VLM-enriched dataset
│
├── db/
│   ├── chroma.sqlite3                # ChromaDB persistent storage
│   ├── a88f4318.../                  # Vector collections
│
└── media/                             # Uploaded inspection images HERE
```

### File Purposes

| File | Purpose |
|------|---------|
| `models.py` | Initializes embeddings (text/image), LLM client, ChromaDB collections |
| `search.py` | Implements RAG pipeline: search → context → report generation |
| `embeddings.py` | Processes dataset: encodes images/text, stores vectors in ChromaDB |
| `data_enrichment.py` | Enriches dataset with VLM analysis (severity, causes, etc.) |
| `build_dataset.py` | Orchestrates dataset building from MBDD2025 |
| `scrape.py` | Parses MBDD2025 YOLO labels with stratified class sampling |
| `main.py` | FastAPI app with prompting endpoint and file upload |

---

## Setup & Installation

### Prerequisites

- Python 3.10+
- Node.js v18+
- OpenRouter API key (for VLM enrichment and LLM analysis)

### Step 1: Clone Repository & Install Dependencies

```bash
git clone https://github.com/aymanea/building-intelligence.git
cd building-intelligence

# Create virtual environment
python -m venv .venv

# Activate virtual environment
# On Windows:
.venv\Scripts\activate
# On macOS/Linux:
source .venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt
```

### Step 2: Download & Prepare Dataset

Download the MBDD2025 (Multi-Building Defect Dataset) from Kaggle:

```bash
# Extract the dataset to: data/raw/MBDD2025/
# Expected structure:
# data/raw/MBDD2025/
# ├── images/     (10,000+ .jpg files)
# └── labels/     (Corresponding .txt files in YOLO format)
```

If using a different dataset, ensure it follows the same directory structure and YOLO label format.

### Step 3: Build and Process the Dataset

**3a. Parse and stratify the raw images:**

```bash
cd src
python build_dataset.py
# Output: data/processed/metadata.csv
```

**3b. Enrich with VLM Analysis** (Optional but recommended)

The system uses Vision Language Models to auto-generate detailed descriptions, severity classifications, and recommendations:

```bash
# Set your OpenRouter API key first
export OPENROUTER_API_KEY="your-api-key-here"
# On Windows PowerShell:
$env:OPENROUTER_API_KEY = "your-api-key-here"

# Run enrichment
python data_enrichment.py
# Output: data/enriched_openrouter.json
# This adds AI-generated expert annotations to the dataset
```

**3c. Build Embeddings & Initialize ChromaDB**

```bash
# Generate embeddings and store vectors in ChromaDB
python embeddings.py
# Output: Vectors stored in db/chroma.sqlite3
# This enables fast similarity search for the RAG system
```

### Step 4: Verify Setup

To verify that the embeddings and database were created successfully:

```bash
# Check that the database exists
ls db/chroma.sqlite3

# Check that processed metadata exists
cat data/processed/metadata.csv | head -10
```

**Note**: Steps 2–4 are one-time setup tasks. Once the embeddings are built and stored in ChromaDB, you do **not** need to repeat them unless you add new images to the dataset.

---

## Usage

### Prerequisites for Running

1. Ensure the setup steps (Steps 1–4) have been completed
2. Prepare your test/inspection image and place it in the `media/` folder
3. Have your OpenRouter API key ready

### Step 1: Start the FastAPI Backend

From the project root directory, start the backend server:

```bash
# Make sure your virtual environment is activated
# .venv\Scripts\activate  (Windows) or source .venv/bin/activate (macOS/Linux)

# Set your OpenRouter API key
export OPENROUTER_API_KEY="your-api-key-here"
# On Windows PowerShell:
$env:OPENROUTER_API_KEY = "your-api-key-here"

# Start the backend server
uvicorn src.main:app --reload --host 0.0.0.0 --port 8000
```

The backend will start at `http://localhost:8000`

**Expected output:**
```
INFO:     Uvicorn running on http://0.0.0.0:8000
INFO:     Application startup complete
```

### Step 2: Start the React Frontend

In a **new terminal** (keep the backend running), navigate to the frontend directory and start the Vite dev server:

```bash
# Navigate to frontend directory
cd frontend

# Install dependencies (if not already done)
npm install

# Start the development server
npm run dev
```

The frontend will start at `http://localhost:5173` (or another port if 5173 is in use)

**Expected output:**
```
  VITE v5.x.x  ready in xxx ms

  ➜  Local:   http://localhost:5173/
```

### Step 3: Prepare Your Test Image

Place the image you want to analyze in the `media/` folder:

```bash
# Example: Copy an image to media/
cp /path/to/your/defect.jpg media/

# Or manually copy your image to:
# building-intelligence/media/your-image.jpg
```

### Step 4: Use the Application

#### Option A: Via Web Interface

1. Open your browser and go to `http://localhost:5173`
2. Upload or select an image from the `media/` folder
3. (Optional) Enter a description or query about the defect
4. Click "Analyze" to get the expert report

#### Option B: Via API (cURL)

**Upload an inspection image:**
```bash
curl -X POST http://localhost:8000/upload-only \
  -F "file=@media/your-image.jpg"

# Response:
# {
#   "path": "media/your-image.jpg",
# }
```

**Analyze via Text Query:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "What defects could cause this type of damage?",
    "img_path": ""
  }'

# Response:
# {
#   "text": "Based on similar cases in the knowledge base, the damage appears to be..."
# }
```

**Analyze via Image:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Analyze this building defect",
    "img_path": "media/your-image.jpg"
  }'

# Response:
# {
#   "text": "Defect Interpretation: ...\nSeverity: ...\nRoot Cause: ..."
# }
```

**Analyze via Text + Image:**
```bash
curl -X POST http://localhost:8000/api/chat \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "This appeared after heavy rain. Is it serious?",
    "img_path": "media/your-image.jpg"
  }'

# Response:
# {
#   "text": "The combination of your description and visual analysis suggests..."
# }
```

### System Workflow

```
1. You upload an image or enter a query (via web UI or API)
    ↓
2. The system converts text + image into embeddings
    ↓
3. Similarity search in ChromaDB retrieves 5 most similar historical cases
    ↓
4. Retrieved cases + your query are sent to the LLM
    ↓
5. LLM generates an expert inspection report
    ↓
6. Report is returned to you with analysis and recommendations
```

---

## API Endpoints

### `GET /`

Health check.

**Response**:
```json
{
  "status": "ok",
  "service": "construction-defect-analysis"
}
```

---

### `POST /upload-only`

Upload an inspection image.

**Parameters**:
- `file` (multipart): Image file (JPEG/PNG)

**Response**:
```json
{
  "path": "media/your_image.jpg",
  "filename": "your_image.jpg"
}
```

---

### `POST /api/chat`

Analyze defects via text and/or image using RAG.

**Request Body**:
```json
{
  "prompt": "string (required)",
  "img_path": "string (optional)"
}
```

**Response**:
```json
{
  "text": "Expert analysis report..."
}
```

---

## What's Production-Ready vs. What Would Be Discarded

### Production-Ready Components

1. **RAG Pipeline** (`search.py`)
   - Robust similarity search
   - Context aggregation
   - LLM integration
   - *Action*: Deploy as-is

2. **Model Initialization** (`models.py`)
   - Reliable ChromaDB setup
   - Proper device management (CPU/GPU)
   - Clean configuration
   - *Action*: Deploy with minor logging additions

3. **FastAPI Server** (`main.py`)
   - Clean endpoints with proper typing
   - CORS support for frontend integration
   - Error handling structure in place
   - *Action*: Add authentication layer, then deploy

4. **Embedding Generation** (`embeddings.py`)
   - Efficient batch processing
   - Error recovery
   - Proper logging
   - *Action*: Deploy with progress tracking UI

### What Would Be Discarded / Replaced

1. **VLM Enrichment Strategy** (`data_enrichment.py`)
   - **Issue**: Depends on external free API (OpenRouter); unreliable for production
   - **Replace**: Build in-house VLM or use Azure/OpenAI


2. **ChromaDB for Scale** (`models.py` DB choice)
   - **Issue**: Not designed for distributed deployments or high throughput
   - **Replace**: Migrate to Pinecone or Weaviate at 500K+ vectors


3. **Manual Sampling Strategy** (`scrape.py`)
   - **Issue**: Hardcoded to 100 samples per class; not dynamic
   - **Replace**: Adaptive sampling based on defect prevalence in real data


4. **React Frontend** (`frontend/`)
   - **Issue**: Just a Vite template; no domain logic
   - **Action**: Replace with proper React app for image upload, search, report viewing


---

## Future Improvements:  What would the project look like in 3 months ?

Moving forward, there are several areas where the project could be significantly improved:

### Data & Validation

Right now, the system relies heavily on VLM-generated annotations for enrichment, which works but isn't ideal. The big gap is real-world inspection data. Ideally, I'd collect and validate hundreds of actual construction inspection reports from field teams—documents with inspector observations, verified defect classifications, severity assessments, and recommended actions. This human-validated data would then replace the synthetic VLM labels, making the RAG system much more reliable and trustworthy.

### LLM Reliability & Hallucination Prevention

One of the main risks with the current system is that the free-tier LLM can occasionally hallucinate or generate incorrect interpretations, especially when given bad inputs like corrupted images or out-of-domain questions. I'd want to build a more robust input validation layer that checks for invalid images (blank, noise, non-construction content), detects contradictions between text and image, and gracefully rejects problematic queries. For the LLM itself, I'd experiment with prompt engineering and hyperparameter tuning (temperature, top_p settings) to reduce hallucinations while keeping responses concise. Adding a confidence scoring system would help flag uncertain analyses and let inspectors know when to exercise human judgment.

### Frontend & User Experience

The current React frontend is pretty basic. I'd want to make it much more interactive and user-friendly: real-time image previews, a gallery of similar retrieved cases for comparison, confidence indicators on reports, better error handling with clear feedback, and proper loading states. For more advanced features, batch image uploads, a history of past inspections, and maybe a simple dashboard showing defect statistics would be nice.

### Production-Grade Features

Eventually, the system would need audit logging to show inspectors exactly which historical cases influenced a decision and why. Role-based access control would let you have different permission levels for inspectors, QA managers, and administrators. There's also API security to consider—JWT authentication, rate limiting, and proper monitoring.

### Scalability & Performance

As the system grows, I'd want to profile and optimize the RAG pipeline to hit response times under 500ms consistently. The vector database choice would likely need revisiting too; while ChromaDB is great for prototyping, migrating to something like Pinecone or Weaviate would be worth considering if the dataset scales beyond 100K vectors. Performance monitoring and automated backups would become essential.

### Testing & Deployment

Finally, adding comprehensive tests (>90% coverage), setting up monitoring with error tracking, and dockerizing the app for cloud deployment would be necessary for production. A proper CI/CD pipeline would make iterations much faster, and an automated data ingestion pipeline would let new inspection images flow into the system without manual work.

The core idea is sound, but the path to production is really about combining real human expertise with the AI system, building in safeguards against mistakes, and making the whole thing reliable and scalable.

---
