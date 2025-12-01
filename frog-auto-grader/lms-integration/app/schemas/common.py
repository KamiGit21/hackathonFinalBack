from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class Grade(BaseModel):
    student_id: int
    student_name: str
    assignment_id: int
    assignment_name: str
    course_name: str
    final_score: float
    status: str  # "APPROVED", "FAILED", etc.


class GradeAuditLog(BaseModel):
    id: int
    assignment_id: int
    assignment_name: str
    student_id: int
    student_name: str
    old_score: float
    new_score: float
    changed_by: str  # profesor o admin
    reason: Optional[str]
    changed_at: datetime
