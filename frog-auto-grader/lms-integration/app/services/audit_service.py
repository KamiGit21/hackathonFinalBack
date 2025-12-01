from app.core.http_client import get_audit_logs_from_assignments
from app.schemas.audit import AuditGradesResponse
from app.schemas.common import GradeAuditLog


async def get_audit_report(year: int) -> AuditGradesResponse:
    raw = await get_audit_logs_from_assignments(year)
    logs = [GradeAuditLog(**item) for item in raw]
    return AuditGradesResponse(year=year, logs=logs)
