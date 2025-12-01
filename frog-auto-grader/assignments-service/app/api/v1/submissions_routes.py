from fastapi import APIRouter, Depends, HTTPException

from app.core.user_context import get_user_context
from app.schemas.submission import SubmissionCreate, SubmissionOut, SubmissionList
from app.services.assignments_service import get_assignment
from app.services.submissions_service import (
    create_submission,
    list_submissions_for_assignment,
)

router = APIRouter(prefix="/assignments", tags=["submissions"])


@router.post("/{assignment_id}/submissions", response_model=SubmissionOut)
def create_submission_endpoint(
    assignment_id: str,
    data: SubmissionCreate,
    user=Depends(get_user_context),
):
    if user["role"] != "STUDENT":
        raise HTTPException(status_code=403, detail="Only students can submit code")

    assignment = get_assignment(assignment_id)
    if not assignment:
        raise HTTPException(status_code=404, detail="Assignment not found")

    payload = create_submission(assignment, user["user_id"], data.code)
    return SubmissionOut(**payload)


@router.get("/{assignment_id}/submissions", response_model=SubmissionList)
def list_submissions_endpoint(
    assignment_id: str,
    user=Depends(get_user_context),
):
    # Aquí podrías limitar por rol (profesor ve todos, estudiante solo los suyos)
    submissions = list_submissions_for_assignment(assignment_id)
    items = [SubmissionOut(**s) for s in submissions]
    return SubmissionList(items=items)
