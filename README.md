# Diabeta Assistant (Diabetes RAG Screening)

A **Retrieval-Augmented Generation (RAG)** assistant for Indonesian diabetes guideline Q&A plus a simple, rule-based **pre-diabetes / type 2 diabetes risk screening** calculator.

> ⚠️ **Medical Disclaimer**
> This tool is for **research and learning only**. It is **not clinically validated** and must **not** be used as medical advice, diagnosis, or treatment. For clinical decisions, consult a licensed healthcare professional.

---

## Features

### 1. Guideline Q&A (RAG)
- Answers diabetes-related questions using **retrieved passages** from provided guideline PDFs.
- Returns the generated answer along with **citations** (source document + page + snippet).
- Supports **English and Bahasa Indonesia** outputs.

### 2. Risk Screening Calculator
- Rule-based risk scoring using:
  - age
  - BMI
  - family history
  - symptom count
- Outputs either **Low / Moderate / High risk** (English) or **Risiko Rendah / Sedang / Tinggi** (Indonesian).

---

## How it works

### RAG pipeline (end-to-end)
Code files:
- `notebooks/loadData.py` — loads guideline PDFs from `data/guidelines/` and splits them into text chunks
- `notebooks/vectorEmbed.py` — embeds chunks and stores them in a local **FAISS** vector database at `vector_db/`
- `notebooks/ragQuery.py` — loads FAISS, retrieves top-k relevant chunks, and asks an LLM to answer using the retrieved context

The FastAPI server (`app.py`) will automatically build the pipeline **on startup** if `vector_db/` is missing.

### Risk screening (rule-based)
Code file:
- `notebooks/riskScreening.py`

The endpoint `POST /screen` calls `calculate_risk(...)` and returns the computed risk string.

---

## Project layout

- `app.py`
  - FastAPI backend
  - Serves the frontend at `/`
  - Provides API endpoints:
    - `POST /chat` (RAG Q&A)
    - `POST /screen` (risk calculator)
- `frontend/`
  - `index.html`, `script.js`, `style.css` for the UI
- `data/`
  - `guidelines/` (PDFs)
  - `processed_texts/` (chunked text, generated)
- `vector_db/`
  - Local FAISS vector index (generated)
- `notebooks/`
  - `loadData.py`, `vectorEmbed.py`, `ragQuery.py`, `riskScreening.py`

---

## API endpoints

### `GET /`
- Returns the single-page frontend (`frontend/index.html`).

### `POST /chat`
Request body:
```json
{
  "question": "...",
  "language": "en" 
}
```
Response:
```json
{
  "answer": "...",
  "citations": [
    {
      "title": "...",
      "page": "...",
      "snippet": "...",
      "url": "http://127.0.0.1:8000/static/<file>.pdf"
    }
  ]
}
```

### `POST /screen`
Request body:
```json
{
  "age": 45,
  "bmi": 26.2,
  "family_history": "yes",
  "symptoms_count": 2,
  "language": "en"
}
```
Response:
```json
{
  "risk": "High Risk (please take a glucose test)"
}
```

---

## Setup

### 1. Prerequisites
- Python 3.11+
- A GROQ API key (used by the LLM in `notebooks/ragQuery.py`)

### 2. Environment variables
Create a `.env` file inside `diabeta-backend/` with:
```bash
GROQ_API_KEY=your_key_here
```

### 3. Install dependencies
```bash
cd diabeta-backend
pip install -r requirements.txt
```

---

## Running locally

### Option A — Start the server (auto-build vector DB if needed)
```bash
uvicorn app:app --reload --host 0.0.0.0 --port 7860
```
Then open:
- http://127.0.0.1:7860/

On first run, if `vector_db/` is missing, the server will execute:
- `python notebooks/loadData.py`
- `python notebooks/vectorEmbed.py`

### Option B — Manually build the vector DB
```bash
python notebooks/loadData.py
python notebooks/vectorEmbed.py
```

---

## Docker

The repository includes a `Dockerfile` that exposes port **7860**.

Build:
```bash
docker build -t diabeta-backend .
```

Run (example):
```bash
docker run --rm -p 7860:7860 \
  -e GROQ_API_KEY="$GROQ_API_KEY" \
  diabeta-backend
```

---

## Notes & gotchas

1. **Vector database location**
   - `vector_db/` is expected in the `diabeta-backend/` folder.

2. **Static guideline PDFs**
   - The backend tries to create citation URLs that map to `frontend/static/<pdf>.pdf`.
   - Ensure guideline PDFs exist and are correctly served if you customize paths.

3. **Language handling**
   - `language` is normalized in the backend.
   - English prompts force English-only output; other languages default to Indonesian prompt.

4. **Risk calculator is heuristic**
   - It is intentionally simple and not a clinical diagnostic tool.

---

## License
Add your license information here (or remove this section).

