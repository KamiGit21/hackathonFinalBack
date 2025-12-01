from pydantic import BaseModel
from typing import List
from app.schemas.common import GradeAuditLog


class AuditGradesResponse(BaseModel):
    year: int
    logs: List[GradeAuditLog]
