from fastapi import FastAPI
from pydantic import BaseModel
from datetime import datetime
import random
import time

from firebase import save_report

app = FastAPI(title="Anti-Plagiarism Microservice")

# ---------------------------
# Request Body
# ---------------------------

class CheckRequest(BaseModel):
    assignment_id: int
    submission_id: int
    code: str

# ---------------------------
# POST /check
# ---------------------------

@app.post("/check")
def check_plagiarism(data: CheckRequest):

    # Simular procesamiento estilo Turnitin
    time.sleep(2)

    max_similarity = random.randint(20, 100)
    suspicious_with = random.sample(range(300, 400), k=2)

    # Datos para guardar en Firebase
    report_data = {
        "assignment_id": data.assignment_id,
        "submission_id": data.submission_id,
        "similar_submission_id": suspicious_with[0],
        "similarity": max_similarity,
        "external_report_url": f"https://fake-turnitin.com/report/{random.randint(1000,9999)}",
        "created_at": datetime.utcnow().isoformat()
    }

    save_report(report_data)

    return {
        "max_similarity": max_similarity,
        "suspicious_with": suspicious_with
    }
