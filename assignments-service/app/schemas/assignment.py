from pydantic import BaseModel
from datetime import datetime
from typing import Any, Optional, List


class AssignmentBase(BaseModel):
    title: str
    description: Optional[str] = None
    course_name: str
    deadline: datetime
    grading_criteria: Optional[Any] = None  # dict/list, se guarda como JSON


class AssignmentCreate(AssignmentBase):
    created_by_id: int  # id del profesor (user_id)


class AssignmentUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    course_name: Optional[str]
    deadline: Optional[datetime]
    grading_criteria: Optional[Any]


class AssignmentOut(AssignmentBase):
    id: int
    created_by_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class AssignmentList(BaseModel):
    items: List[AssignmentOut]
