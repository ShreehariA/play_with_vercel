# api/index.py
from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import json
from pathlib import Path

app = FastAPI()

# Enable CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allow all methods
    allow_headers=["*"],  # Allow all headers
)

def load_student_data():
    try:
        json_path = Path(__file__).parent / 'q-vercel-python.json'
        with open(json_path, 'r') as file:
            data = json.load(file)
        return {student["name"]: student["marks"] for student in data}
    except Exception as e:
        print(f"Error loading data: {e}")
        return {}

# Load the data once when the app starts
STUDENT_DICT = load_student_data()

@app.get("/api")
async def get_marks(name: list[str] = Query(...)):
    marks = [STUDENT_DICT.get(n, 0) for n in name]
    return {"marks": marks}

@app.get("/")
async def read_root():
    return {
        "message": "Hello! Use /api endpoint with name query parameters to get marks.",
        "example": "/api?name=StudentName1&name=StudentName2"
    }