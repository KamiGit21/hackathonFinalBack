from fastapi import APIRouter, Depends, HTTPException, Query

from app.core.user_context import get_user_context
from app.schemas.audit import AuditGradesResponse, GradeAuditLogOut
from app.services.audit_service import list_audit_logs_for_year

router = APIRouter(prefix="/audit", tags=["audit"])


@router.get("/grades", response_model=AuditGradesResponse)
def get_audit_grades_endpoint(
    year: int = Query(..., description="Año académico para reporte de auditoría"),
    user=Depends(get_user_context),
):
    if user["role"] not in ("ADMIN", "TEACHER"):
        raise HTTPException(status_code=403, detail="Not allowed to view audit logs")

    logs = list_audit_logs_for_year(year)
    items = [GradeAuditLogOut(**l) for l in logs]
    return AuditGradesResponse(year=year, logs=items)
