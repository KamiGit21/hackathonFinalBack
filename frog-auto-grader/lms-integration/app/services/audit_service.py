from app.core.http_client import get_audit_logs_from_assignments
from app.schemas.audit import AuditGradesResponse
from app.schemas.common import GradeAuditLog


async def get_audit_report(year: int) -> AuditGradesResponse:
    """
    Consume /audit/grades del assignments-service y lo adapta
    al modelo local de auditoría.
    """
    raw = await get_audit_logs_from_assignments(year)
    logs_data = raw.get("logs", [])
    logs = [GradeAuditLog(**item) for item in logs_data]
    return AuditGradesResponse(year=raw.get("year", year), logs=logs)
