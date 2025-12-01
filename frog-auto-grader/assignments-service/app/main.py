from fastapi import FastAPI

from app.api.v1.assignments_routes import router as assignments_router
from app.api.v1.submissions_routes import router as submissions_router
from app.api.v1.audit_routes import router as audit_router

app = FastAPI(
    title="Assignments Service",
    version="1.0.0",
    description="Microservicio para tareas, envíos, notas y auditoría (Firestore).",
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "assignments-service"}


# Rutas v1
app.include_router(assignments_router, prefix="/api/v1")
app.include_router(submissions_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
