from fastapi import FastAPI

from app.api.v1.lms_routes import router as lms_router
from app.api.v1.audit_routes import router as audit_router

app = FastAPI(
    title="LMS Integration & Audit Service",
    version="1.0.0",
    description="Microservicio para integración con LMS legacy y auditoría anual de notas."
)


@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok", "service": "lms-integration"}


# Incluir routers versión 1
app.include_router(lms_router, prefix="/api/v1")
app.include_router(audit_router, prefix="/api/v1")
