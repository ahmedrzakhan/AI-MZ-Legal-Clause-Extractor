# AI-MZ Legal Clause Extractor

![AI-MZ Legal Clause Extractor](https://img.shields.io/badge/Project-AI--MZ_Legal_Clause_Extractor-blue) ![Python](https://img.shields.io/badge/Language-Python-3776AB.svg)

Welcome to the **Legal Clause Extractor**, a powerful tool designed to extract key legal clauses (Confidentiality, Indemnity, and Termination) from PDF contracts. Built with Python, this project leverages natural language processing (NLP), a RESTful API with FastAPI, a user-friendly Streamlit UI, and MongoDB for data persistence. This solution is perfect for legal professionals, developers, and businesses looking to automate contract analysis.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
  - [Streamlit UI](#streamlit-ui)
  - [FastAPI API](#fastapi-api)
- [Project Structure](#project-structure)
- [Contributing](#contributing)
- [License](#license)
- [Acknowledgements](#acknowledgements)

## Features

- **Clause Extraction**: Automatically identifies and extracts Confidentiality, Indemnity, and Termination clauses from PDF contracts.
- **User-Friendly Interface**: Streamlit-based web UI for easy file uploads and result visualization.
- **RESTful API**: FastAPI endpoint (`/extract-clauses`) for programmatic access and integration.
- **Data Persistence**: Stores extracted clauses in MongoDB for future retrieval and analysis.
- **Robust Processing**: Handles multi-sentence clauses, preserves original capitalization, and eliminates extra spaces or artifacts.
- **Scalable Design**: Supports both manual (UI) and automated (API) use cases.

## Installation

### Prerequisites

- Python 3.8+
- MongoDB (Community Edition)

### Setup Steps

1. **Clone the Repository**:

   ```bash
   git clone https://github.com/ahmedrzakhan/Legal-Clause-Extraction-Tool.git
   cd Legal-Clause-Extraction-Tool
   ```

2. **Install Dependencies**:

```bash
pip3 install -r requirements.txt
```

Download the spaCy model:

```bash
python3 -m spacy download en_core_web_sm
```

2. **Install MongoDB**:
1. Download and install MongoDB Community Server from mongodb.com.
1. Start the MongoDB service:

```bash
brew services start mongodb-community  # macOS with Homebrew
```

## Usage

### Streamlit UI

1. Run the UI:

```bash
streamlit run ui.py
```

2. Open your browser at http://localhost:8501.

3. Upload a PDF:

   - Use the "Choose a PDF file" or drag-and-drop option to upload a contract (e.g., dummy_contract.pdf).
   - Click "Extract Clauses" to process the file.

4. View Results:
   - The extracted clauses will be displayed in JSON format.
   - Optionally, check "Show All Stored Contracts" to view data saved in MongoDB.

### FastAPI API

1. Run the API:

```bash
python3 main.py
```

The server will start at http://0.0.0.0:8000.

2. Test with Postman or cURL:
   - Postman:
     - Method: POST
     - URL: http://localhost:8000/extract-clauses
     - Body: form-data, key file, value as your PDF file (select as "File").
   - cURL:

```bash
curl -X POST -F "file=@/path/to/dummy_contract.pdf" http://localhost:8000/extract-clauses
```

3. Expected Response:

```json
{
  "confidentiality": "All parties agree to keep info secret.",
  "indemnity": "Party A shall indemnify Party B for losses.",
  "termination": "This ends with 30 days notice."
}
```

## Project Structure

```text
Legal-Clause-Extraction-Tool/
├── main.py              # FastAPI REST API
├── ui.py                # Streamlit UI
├── dummy_contract.pdf   # Sample PDF for testing
├── requirements.txt     # Python dependencies
└── README.md            # This file
```
