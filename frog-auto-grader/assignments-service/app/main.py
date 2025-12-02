from fastapi import FastAPI

from app.api.v1.assignments_routes import router as assignments_router
from app.api.v1.submissions_routes import router as submissions_router
from app.api.v1.audit_routes import router as audit_router


tags_metadata = [
    {
        "name": "health",
        "description": "Verificación del estado del servicio."
    },
    {
        "name": "assignments",
        "description": "Gestión de tareas (crear, listar, actualizar, eliminar)."
    },
    {
        "name": "submissions",
        "description": "Gestión de envíos y calificaciones de los estudiantes."
    },
    {
        "name": "audit",
        "description": "Auditoría de cambios y notas almacenadas en Firestore."
    },
]

app = FastAPI(
    title="Assignments Service",
    version="1.0.0",
    description="Microservicio para tareas, envíos, notas y auditoría (Firestore).",
    openapi_tags=tags_metadata,
    docs_url="/docs",     # Swagger UI
    redoc_url="/redoc"    # ReDoc
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "assignments-service"}


# Rutas v1
app.include_router(assignments_router, prefix="/api/v1", tags=["assignments"])
app.include_router(submissions_router, prefix="/api/v1", tags=["submissions"])
app.include_router(audit_router, prefix="/api/v1", tags=["audit"])
