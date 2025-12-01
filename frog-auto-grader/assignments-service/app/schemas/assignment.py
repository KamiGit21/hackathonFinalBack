from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional, List


class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    course: str
    deadline: datetime
    grading_criteria: Optional[Any] = None  # dict/list para pruebas, rubricas


class AssignmentCreate(AssignmentBase):
    pass  # el created_by viene del contexto de usuario


class AssignmentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    course: Optional[str]
    deadline: Optional[datetime]
    grading_criteria: Optional[Any]


class AssignmentOut(AssignmentBase):
    id: str
    created_by: str
    created_at: datetime


class AssignmentList(BaseModel):
    items: List[AssignmentOut]
