from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class GradeAuditLogOut(BaseModel):
    id: str
    submission_id: str
    assignment_id: str
    student_id: str
    old_score: Optional[float]
    new_score: float
    changed_by: str
    reason: Optional[str]
    changed_at: datetime


class AuditGradesResponse(BaseModel):
    year: int
    logs: List[GradeAuditLogOut]
