import warnings
warnings.filterwarnings("ignore", category=UserWarning)

import PyPDF2
import spacy
import json
import unicodedata
from fastapi import FastAPI, UploadFile, File
import uvicorn
import os
from pymongo import MongoClient
import datetime

app = FastAPI()
nlp = spacy.load("en_core_web_sm")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_clauses_db"]
collection = db["contracts"]

def read_pdf(file_path):
    with open(file_path, "rb") as file:
        pdf_reader = PyPDF2.PdfReader(file)
        text = "".join(page.extract_text() for page in pdf_reader.pages)
        text = unicodedata.normalize("NFKD", text).replace("\n", " ")
        text = text.replace(".", ". ").replace("  ", " ")
        return text

def extract_clauses(text):
    doc = nlp(text)
    clauses = {"confidentiality": "", "indemnity": "", "termination": ""}
    clause_keywords = {
        "confidentiality": "confidentiality",
        "indemnity": "indemnity",
        "termination": "termination"
    }
    current_clause = None

    for sent in doc.sents:
        sent_text_lower = unicodedata.normalize("NFKD", sent.text).lower().strip()
        for clause, keyword in clause_keywords.items():
            if keyword in sent_text_lower and not clauses[clause]:
                current_clause = clause
                keyword_pos = sent_text_lower.find(keyword)
                if keyword_pos != -1:
                    start_pos = keyword_pos + len(keyword)
                    colon_pos = sent.text.find(":", keyword_pos)
                    clauses[clause] = sent.text[colon_pos + 1:].strip() if colon_pos != -1 and colon_pos >= start_pos else sent.text[start_pos:].strip()
        if current_clause and not any(keyword in sent_text_lower for keyword in clause_keywords.values()):
            clauses[current_clause] += " " + sent.text.strip()

    for clause in clauses:
        clauses[clause] = clauses[clause].strip()

    return clauses

@app.post("/extract-clauses")
async def extract_clauses_api(file: UploadFile = File(...)):
    try:
        # Save uploaded file temporarily
        file_path = "temp.pdf"
        with open(file_path, "wb") as buffer:
            buffer.write(await file.read())

        # Extract text and clauses
        text = read_pdf(file_path)
        clauses = extract_clauses(text)

        # Store in MongoDB with filename as ID
        document = {"filename": file.filename, "clauses": clauses, "timestamp": datetime.datetime.now()}
        collection.insert_one(document)

        os.remove(file_path)

        return clauses
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)