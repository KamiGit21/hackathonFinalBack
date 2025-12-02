from datetime import datetime, timezone
from typing import Dict, Any, List, Optional

from app.core.firebase import db
from app.services.audit_service import log_grade_change


def _get_next_attempt_number(assignment_id: str, student_id: str) -> int:
    """
    Obtiene el siguiente número de intento para un estudiante en una tarea.
    NO usa order_by para no requerir índices compuestos en Firestore.
    """
    docs = (
        db.collection("submissions")
        .where("assignment_id", "==", assignment_id)
        .where("student_id", "==", student_id)
        .stream()
    )

    max_attempt = 0
    for doc in docs:
        data = doc.to_dict()
        attempt = data.get("attempt_number", 0)
        if attempt > max_attempt:
            max_attempt = attempt

    return max_attempt + 1


def create_submission(assignment: Dict[str, Any], student_id: str, code: str) -> Dict[str, Any]:
    """
    Crea un submission nuevo:
    - Calcula attempt_number
    - Marca PENDING o REJECTED_DEADLINE según deadline
    """
    now = datetime.now(timezone.utc)
    deadline = assignment.get("deadline")

    status = "PENDING"

    # deadline viene de Firestore como datetime (normalmente con tzinfo=UTC)
    if isinstance(deadline, datetime):
        if deadline.tzinfo is None:
            deadline_utc = deadline.replace(tzinfo=timezone.utc)
        else:
            deadline_utc = deadline

        if now > deadline_utc:
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
        .stream()
    )

    result: List[Dict[str, Any]] = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)

    # ordenar en Python por fecha de creación (más reciente primero)
    result.sort(key=lambda x: x.get("created_at"), reverse=True)
    return result


def update_submission_score(
    submission_id: str,
    new_score: float,
    changed_by: str,
    reason: Optional[str] = None,
) -> Optional[Dict[str, Any]]:
    """
    Actualiza el score de un submission y registra auditoría.
    """
    ref = db.collection("submissions").document(submission_id)
    snap = ref.get()

    if not snap.exists:
        return None

    data = snap.to_dict()
    old_score = data.get("score")

    ref.update(
        {
            "score": new_score,
            "status": "GRADED",
        }
    )

    # registrar auditoría
    log_grade_change(
        submission_id=submission_id,
        assignment_id=data.get("assignment_id"),
        student_id=data.get("student_id"),
        old_score=old_score,
        new_score=new_score,
        changed_by=changed_by,
        reason=reason,
    )

    updated = ref.get().to_dict()
    updated["id"] = ref.id
    return updated
