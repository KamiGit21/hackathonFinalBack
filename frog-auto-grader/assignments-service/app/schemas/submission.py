from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class SubmissionCreate(BaseModel):
    code: str


class SubmissionOut(BaseModel):
    id: str
    assignment_id: str
    student_id: str
    attempt_number: int
    code: str
    status: str
    score: Optional[float]
    created_at: datetime


class SubmissionList(BaseModel):
    items: List[SubmissionOut]


class SubmissionGradeUpdate(BaseModel):
    score: float
    reason: Optional[str] = None
