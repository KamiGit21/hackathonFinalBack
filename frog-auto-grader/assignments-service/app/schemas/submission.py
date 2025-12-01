from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List


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
