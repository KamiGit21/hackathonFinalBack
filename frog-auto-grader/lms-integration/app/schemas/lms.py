from pydantic import BaseModel
from typing import List
from app.schemas.common import Grade


class LmsGradesResponse(BaseModel):
    assignment_id: str
    format: str  # "json" o "csv"
    grades: List[Grade]


class LmsSyncResult(BaseModel):
    assignment_id: str
    sent_to_lms: bool
    message: str
