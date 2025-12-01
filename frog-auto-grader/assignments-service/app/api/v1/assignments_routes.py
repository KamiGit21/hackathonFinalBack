from fastapi import APIRouter, Depends, HTTPException
from typing import List

from app.core.user_context import get_user_context
from app.schemas.assignment import (
    AssignmentCreate,
    AssignmentUpdate,
    AssignmentOut,
    AssignmentList,
)
from app.schemas.grade import GradeList
from app.services.assignments_service import (
    create_assignment,
    list_assignments,
    get_assignment,
    update_assignment,
)
from app.services.grades_service import get_final_grades_for_assignment

router = APIRouter(prefix="/assignments", tags=["assignments"])


@router.post("/", response_model=AssignmentOut)
def create_assignment_endpoint(
    data: AssignmentCreate,
    user=Depends(get_user_context),
):
    if user["role"] != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can create assignments")

    payload = create_assignment(
        {
            **data.dict(),
            "created_by": user["user_id"],
        }
    )
    return AssignmentOut(**payload)


@router.get("/", response_model=AssignmentList)
def list_assignments_endpoint():
    items = [AssignmentOut(**a) for a in list_assignments()]
    return AssignmentList(items=items)


@router.get("/{assignment_id}", response_model=AssignmentOut)
def get_assignment_endpoint(assignment_id: str):
    data = get_assignment(assignment_id)
    if not data:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return AssignmentOut(**data)


@router.patch("/{assignment_id}", response_model=AssignmentOut)
def update_assignment_endpoint(
    assignment_id: str,
    data: AssignmentUpdate,
    user=Depends(get_user_context),
):
    if user["role"] != "TEACHER":
        raise HTTPException(status_code=403, detail="Only teachers can update assignments")

    updated = update_assignment(assignment_id, data.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Assignment not found")
    return AssignmentOut(**updated)


@router.get("/{assignment_id}/grades", response_model=GradeList)
def get_assignment_grades_endpoint(assignment_id: str):
    """
    Endpoint consumido por el lms-integration-service.
    No requiere auth complejo, solo el assignment_id.
    """
    grades = get_final_grades_for_assignment(assignment_id)
    return GradeList(assignment_id=assignment_id, items=grades)
