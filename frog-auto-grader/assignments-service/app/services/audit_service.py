from datetime import datetime
from typing import Optional, List, Dict, Any

from app.core.firebase import db


def log_grade_change(
    submission_id: str,
    assignment_id: str,
    student_id: str,
    old_score: Optional[float],
    new_score: float,
    changed_by: str,
    reason: Optional[str] = None,
):
    db.collection("grade_audit_logs").add(
        {
            "submission_id": submission_id,
            "assignment_id": assignment_id,
            "student_id": student_id,
            "old_score": old_score,
            "new_score": new_score,
            "changed_by": changed_by,
            "reason": reason,
            "changed_at": datetime.utcnow(),
        }
    )


def list_audit_logs_for_year(year: int) -> List[Dict[str, Any]]:
    start = datetime(year, 1, 1)
    end = datetime(year + 1, 1, 1)

    docs = (
        db.collection("grade_audit_logs")
        .where("changed_at", ">=", start)
        .where("changed_at", "<", end)
        .stream()
    )

    result = []
    for doc in docs:
        d = doc.to_dict()
        d["id"] = doc.id
        result.append(d)
    return result
