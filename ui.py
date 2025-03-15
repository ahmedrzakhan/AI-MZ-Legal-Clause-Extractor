import streamlit as st
import PyPDF2
import spacy
import unicodedata
import json
from pymongo import MongoClient
import datetime

nlp = spacy.load("en_core_web_sm")

# MongoDB connection
client = MongoClient("mongodb://localhost:27017/")
db = client["legal_clauses_db"]
collection = db["contracts"]

def read_pdf(file):
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

st.title("AI-MZ Legal Clause Extractor")
st.write("Upload a PDF contract to extract clauses.")

uploaded_file = st.file_uploader("Choose a PDF file", type="pdf")
if uploaded_file is not None:
    if st.button("Extract Clauses"):
        with st.spinner("Processing..."):
            text = read_pdf(uploaded_file)
            clauses = extract_clauses(text)
            # Store in MongoDB
            document = {"filename": uploaded_file.name, "clauses": clauses, "timestamp": datetime.datetime.now()}
            collection.insert_one(document)
            st.success("Extraction complete!")
            st.json(clauses)

# Optional: Display all stored contracts
if st.checkbox("Show All Stored Contracts"):
    contracts = list(collection.find())
    st.json(contracts)