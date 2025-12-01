from pydantic import BaseModel
from typing import List


class GradeOut(BaseModel):
    student_id: str
    assignment_id: str
    final_score: float
    status: str  # APPROVED / FAILED


class GradeList(BaseModel):
    assignment_id: str
    items: List[GradeOut]
