# DOCTALK
DOCTALK: Discuss Research Papers Locally with LLM and RAG

# Project Description

## File Contents

- **backend/app.py**: The main application file for the backend, built with the Flask framework. It handles HTTP requests and interacts with the LLM model and vector database.
- **backend/model_utils.py**: A utility class for managing and loading the sentence vector model.
- **backend/pdf_processor.py**: A module responsible for parsing PDF files and extracting text.
- **backend/text_splitter.py**: A utility class for splitting text into smaller chunks.
- **backend/vectorDB.py**: A module for interacting with the vector database.
- **frontend**: The frontend code directory, built with React and Vite, containing UI components and configuration files.

## Compilation and Running Steps

### Pre-requisites

1. **Download Models**: 
   - Ensure you download the LLM model and place it in the path specified in `backend/model_utils.py`. You can check the specific path in the `MODEL_PATH` variable.
   - The vector database and vector model do not require additional downloads; they are handled automatically by the code.

### Backend

1. Navigate to the `backend` directory.
2. Install Python dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Start the Flask application:
   ```bash
   python app.py
   ```

### Frontend

1. Navigate to the `frontend` directory.
2. Install Node.js dependencies:
   ```bash
   npm install
   ```
3. Start the development server:
   ```bash
   npm run dev
   ```
