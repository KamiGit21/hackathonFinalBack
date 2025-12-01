from fastapi import APIRouter, Query
from app.services.audit_service import get_audit_report
from app.schemas.audit import AuditGradesResponse

router = APIRouter(
    prefix="/audit",
    tags=["audit"]
)


@router.get("/grades", response_model=AuditGradesResponse)
async def get_audit_grades(
    year: int = Query(..., description="Año académico para reporte de auditoría"),
):
    """
    Devuelve el reporte de auditoría de calificaciones para un año específico.
    Este endpoint será usado para mostrar a entidades estatales los cambios de notas.
    """
    report = await get_audit_report(year)
    return report
