# DOCTALK
Discuss Research Papers Locally with LLM and RAG

## Overview
DOCTALK is a full-stack application that enables users to upload and interact with
research papers in PDF format through a locally deployed Large Language Model (LLM).
The system uses a Retrieval-Augmented Generation (RAG) pipeline to provide
context-aware responses grounded in document content, without relying on external
LLM APIs.

## Key Features
- PDF document upload and text extraction
- Document ingestion and chunking for long documents
- Vector-based retrieval using embeddings
- LLM-powered question answering grounded in retrieved document content
- Fully local inference for privacy-sensitive use cases
- Web-based interface built with React

## System Architecture
The system follows a standard RAG pipeline:
1. PDF parsing and text extraction
2. Text chunking and embedding generation
3. Vector database indexing and retrieval
4. Context-aware response generation using a local LLM

## Tech Stack
- Backend: Python, Flask
- Frontend: React, Vite
- LLM: Local LLM (configured in `model_utils.py`)
- Embeddings & Vector Search: Sentence embedding model + vector database
- Containerization: Docker

## Project Structure
backend/
├── app.py # Flask API and request handling
├── model_utils.py # LLM and embedding model management
├── pdf_processor.py # PDF parsing and text extraction
├── text_splitter.py # Text chunking utilities
├── vectorDB.py # Vector database interface
frontend/ # React + Vite frontend


## Setup & Run

### Prerequisites
- Python 3.9+
- Node.js 18+

### Backend
```bash
cd backend
pip install -r requirements.txt
python app.py
```

### Frontend
```bash
cd frontend
npm install
npm run dev
```

## Note
The LLM model path can be configured via MODEL_PATH in backend/model_utils.py
The vector database and embedding model are initialized automatically at runtime
