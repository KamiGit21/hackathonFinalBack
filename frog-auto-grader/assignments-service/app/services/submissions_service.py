from datetime import datetime
from typing import Dict, Any, List

from firebase_admin import firestore

from app.core.firebase import db


def _get_next_attempt_number(assignment_id: str, student_id: str) -> int:
    query = (
        db.collection("submissions")
        .where("assignment_id", "==", assignment_id)
        .where("student_id", "==", student_id)
        .order_by("attempt_number", direction=firestore.Query.DESCENDING)
        .limit(1)
        .stream()
    )

    for doc in query:
        return doc.to_dict().get("attempt_number", 0) + 1
    return 1


def create_submission(assignment: Dict[str, Any], student_id: str, code: str) -> Dict[str, Any]:
    now = datetime.utcnow()
    deadline = assignment["deadline"]

    status = "PENDING"
    if isinstance(deadline, datetime) and now > deadline:
        status = "REJECTED_DEADLINE"

    attempt_number = _get_next_attempt_number(assignment["id"], student_id)

    ref = db.collection("submissions").document()
    payload = {
        "assignment_id": assignment["id"],
        "student_id": student_id,
        "attempt_number": attempt_number,
        "code": code,
        "status": status,
        "score": None,
        "created_at": now,
    }
    ref.set(payload)
    payload["id"] = ref.id
    return payload


def list_submissions_for_assignment(assignment_id: str) -> List[Dict[str, Any]]:
    docs = (
        db.collection("submissions")
        .where("assignment_id", "==", assignment_id)
        .order_by("created_at", direction=firestore.Query.DESCENDING)
        .stream()
    )

    result = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)
    return result
