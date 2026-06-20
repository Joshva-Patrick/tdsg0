from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import csv

app = FastAPI()

# Enable CORS for all origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET"],
    allow_headers=["*"],
)

CSV_FILE = "q-fastapi.csv"


@app.get("/api")
def get_students(class_: list[str] | None = Query(None, alias="class")):

    students = []

    with open(CSV_FILE, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            # No filter -> return all students
            if class_ is None:
                students.append(row)

            # Filter by one or more classes
            elif row["class"] in class_:
                students.append(row)

    return students

