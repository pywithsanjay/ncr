
from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime
import uuid
import json
import os

app = FastAPI(title="Student Tutor API")


STUDENT_FILE = "data.json"
TUTOR_FILE   = "tutordata.json"


def load_data(file_path):
    if not os.path.exists(file_path):
        return []
    try:
        with open(file_path, "r") as f:
            return json.load(f)
    except json.JSONDecodeError:
        return []

def save_data(file_path, data):
    with open(file_path, "w") as f:
        json.dump(data, f, indent=4)

def generate_id():
    return str(uuid.uuid4())



@app.post("/student")
def add_student(data: UserBase, request: Request):
    records = load_data(STUDENT_FILE)

    record = {
        "id": generate_id(),
        "type": "student",

        "name": data.name,
        "mobile_no": data.mobile_no,
        "email": data.email,
        "course": data.course,
        "subject": data.subject,

        "qualification": data.qualification,
        "experience": data.experience,
        "preferred_mode": data.preferred_mode,
        "language": data.language,

        "country": data.country,
        "city": data.city,
        "timezone": data.timezone,

        "status": "active",
        "joined_date": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": None,

        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "source": "website"
    }

    records.append(record)
    save_data(STUDENT_FILE, records)

    return {"message": "Student added successfully", "data": record}


@app.post("/tutor")
def add_tutor(data: UserBase, request: Request):
    records = load_data(TUTOR_FILE)

    record = {
        "id": generate_id(),
        "type": "tutor",

        "name": data.name,
        "mobile_no": data.mobile_no,
        "email": data.email,
        "course": data.course,
        "subject": data.subject,

        "qualification": data.qualification,
        "experience": data.experience,
        "preferred_mode": data.preferred_mode,
        "language": data.language,

        "country": data.country,
        "city": data.city,
        "timezone": data.timezone,

        "status": "active",
        "joined_date": datetime.utcnow().isoformat(),
        "created_at": datetime.utcnow().isoformat(),
        "updated_at": None,

        "ip_address": request.client.host,
        "user_agent": request.headers.get("user-agent"),
        "source": "website"
    }

    records.append(record)
    save_data(TUTOR_FILE, records)

    return {"message": "Tutor added successfully", "data": record}
