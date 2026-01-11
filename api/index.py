from fastapi import FastAPI, Request, HTTPException
from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime
import uuid
import json
import os

app = FastAPI(title="Student & Tutor API")

# ------------------------
# File paths
# ------------------------
STUDENT_FILE = "data.json"
TUTOR_FILE   = "tutordata.json"

# ------------------------
# Helper functions
# ------------------------
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

# ------------------------
# Pydantic Models
# ------------------------
class UserBase(BaseModel):
    name: str
    mobile_no: str
    email: EmailStr
    course: str
    subject: str

    qualification: Optional[str] = None
    experience: Optional[str] = None
    preferred_mode: Optional[str] = "online"
    language: Optional[str] = "English"

    country: Optional[str] = None
    city: Optional[str] = None
    timezone: Optional[str] = None


class UpdateUser(BaseModel):
    name: Optional[str]
    mobile_no: Optional[str]
    course: Optional[str]
    subject: Optional[str]

    qualification: Optional[str]
    experience: Optional[str]
    preferred_mode: Optional[str]
    language: Optional[str]

    country: Optional[str]
    city: Optional[str]
    timezone: Optional[str]

    status: Optional[str]

# ------------------------
# Routes
# ------------------------
@app.get("/")
def home():
    return {
        "message": "FastAPI running successfully",
        "routes": [
            "POST /student",
            "POST /tutor",
            "GET /students",
            "GET /tutors",
            "PUT /student/{id}",
            "PUT /tutor/{id}"
        ]
    }

# ------------------------
# CREATE STUDENT
# ------------------------
@app.post("/student")
def create_student(data: UserBase, request: Request):
    try:
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

            "ip_address": get_client_ip(request),
            "user_agent": request.headers.get("user-agent", "unknown"),
            "source": "website"
        }

        records.append(record)
        save_data(STUDENT_FILE, records)

        return {"message": "Student created", "data": record}

    except Exception as e:
        # 🔥 THIS will surface the real error
        raise HTTPException(status_code=500, detail=str(e))
# ------------------------
# CREATE TUTOR
# ------------------------
@app.post("/tutor")
def create_tutor(data: UserBase, request: Request):
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

    return {"message": "Tutor created", "data": record}

# ------------------------
# GET STUDENTS
# ------------------------
@app.get("/students")
def get_students():
    data = load_data(STUDENT_FILE)
    return {"count": len(data), "data": data}

# ------------------------
# GET TUTORS
# ------------------------
@app.get("/tutors")
def get_tutors():
    data = load_data(TUTOR_FILE)
    return {"count": len(data), "data": data}

# ------------------------
# UPDATE STUDENT
# ------------------------
@app.put("/student/{user_id}")
def update_student(user_id: str, data: UpdateUser):
    records = load_data(STUDENT_FILE)

    for record in records:
        if record["id"] == user_id:
            for key, value in data.dict(exclude_unset=True).items():
                record[key] = value

            record["updated_at"] = datetime.utcnow().isoformat()
            save_data(STUDENT_FILE, records)

            return {"message": "Student updated", "data": record}

    raise HTTPException(status_code=404, detail="Student not found")

# ------------------------
# UPDATE TUTOR
# ------------------------
@app.put("/tutor/{user_id}")
def update_tutor(user_id: str, data: UpdateUser):
    records = load_data(TUTOR_FILE)

    for record in records:
        if record["id"] == user_id:
            for key, value in data.dict(exclude_unset=True).items():
                record[key] = value

            record["updated_at"] = datetime.utcnow().isoformat()
            save_data(TUTOR_FILE, records)

            return {"message": "Tutor updated", "data": record}

    raise HTTPException(status_code=404, detail="Tutor not found")

