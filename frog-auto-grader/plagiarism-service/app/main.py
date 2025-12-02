from fastapi import FastAPI
from pydantic import BaseModel, Field
from datetime import datetime
import random
import time

from app.firebase import save_report  # Ajusta según tu estructura de paquetes

app = FastAPI(
    title="Anti-Plagiarism Microservice",
    description="Microservicio que simula un chequeo de plagio para submissions de assignments. "
                "Permite subir código, genera un porcentaje de similitud aleatorio y guarda un registro en Firebase.",
    version="1.0.0"
)

# ---------------------------
# Request Model
# ---------------------------

class CheckRequest(BaseModel):
    assignment_id: int = Field(..., example=10, description="ID del assignment a verificar")
    submission_id: int = Field(..., example=55, description="ID de la submission a verificar")
    code: str = Field(..., example="print('hola mundo')", description="Código de la submission a analizar")

# ---------------------------
# Response Model
# ---------------------------

class CheckResponse(BaseModel):
    max_similarity: int = Field(..., example=82, description="Porcentaje máximo de similitud detectado")
    suspicious_with: list[int] = Field(..., example=[321, 322], description="IDs de submissions sospechosas de plagio")

# ---------------------------
# POST /check
# ---------------------------

@app.post(
    "/check",
    response_model=CheckResponse,
    summary="Revisar submission por posible plagio",
    description="Simula un análisis de plagio. Retorna un porcentaje de similitud aleatorio "
                "y las submissions sospechosas. Guarda el resultado en Firebase."
)
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

    return CheckResponse(
        max_similarity=max_
