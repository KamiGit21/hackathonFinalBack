from fastapi import FastAPI

from app.api.v1.lms_routes import router as lms_router
from app.api.v1.audit_routes import router as audit_router

# Tags para organizar la doc en Swagger
tags_metadata = [
    {
        "name": "health",
        "description": "Endpoints de verificación de estado del servicio."
    },
    {
        "name": "lms",
        "description": "Operaciones relacionadas con la integración con el LMS legacy."
    },
    {
        "name": "audit",
        "description": "Endpoints para la auditoría anual de notas."
    },
]

app = FastAPI(
    title="LMS Integration & Audit Service",
    version="1.0.0",
    description="Microservicio para integración con LMS legacy y auditoría anual de notas.",
    openapi_tags=tags_metadata,
    docs_url="/docs",      # Swagger UI
    redoc_url="/redoc"     # ReDoc
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "lms-integration"}


# Incluir routers versión 1
app.include_router(lms_router, prefix="/api/v1", tags=["lms"])
app.include_router(audit_router, prefix="/api/v1", tags=["audit"])
