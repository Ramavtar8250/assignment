cd from fastapi import FastAPI, File, UploadFile, HTTPException, Form
from fastapi.responses import JSONResponse
from fastapi.middleware.cors import CORSMiddleware
import fitz  # PyMuPDF
import os
from langchain import LangChain
from llama_index import LLamaIndex
from typing import Optional
import sqlite3
from datetime import datetime

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

DATABASE = "docs.db"
UPLOAD_FOLDER = "uploads"
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Initialize LangChain/LLamaIndex for NLP (pseudo-code)
lang_chain = LangChain()  # Replace with LangChain setup
llama_index = LLamaIndex()  # Replace with LLamaIndex setup

# Database setup
def init_db():
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS documents 
                      (id INTEGER PRIMARY KEY, filename TEXT, upload_date TEXT)''')
    conn.commit()
    conn.close()

init_db()

# PDF Upload Endpoint
@app.post("/upload_pdf/")
async def upload_pdf(file: UploadFile = File(...)):
    if file.content_type != "application/pdf":
        raise HTTPException(status_code=400, detail="Only PDF files are allowed.")

    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    with open(file_path, "wb") as buffer:
        buffer.write(await file.read())

    # Save metadata to database
    conn = sqlite3.connect(DATABASE)
    cursor = conn.cursor()
    cursor.execute("INSERT INTO documents (filename, upload_date) VALUES (?, ?)", 
                   (file.filename, datetime.now().strftime("%Y-%m-%d %H:%M:%S")))
    conn.commit()
    conn.close()

    return {"filename": file.filename, "status": "uploaded"}

# PDF Text Extraction and Answering
@app.post("/ask_question/")
async def ask_question(filename: str = Form(...), question: str = Form(...)):
    file_path = os.path.join(UPLOAD_FOLDER, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found.")

    # Extract text from PDF
    text_content = ""
    with fitz.open(file_path) as pdf:
        for page_num in range(pdf.page_count):
            page = pdf[page_num]
            text_content += page.get_text()

    # Process the question with LangChain/LLamaIndex
    answer = lang_chain.ask(question, context=text_content)  # Replace with actual NLP setup

    return JSONResponse({"answer": answer})
from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World"}
