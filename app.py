from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = "q-fastapi.csv"


@app.get("/api")
def get_students(class_: list[str] | None = Query(default=None, alias="class")):

    students = []

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            if class_ is None or row["class"] in class_:
                students.append({
                    "studentId": int(row["studentId"]),
                    "class": row["class"]
                })

    return {"students": students}