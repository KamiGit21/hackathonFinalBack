from typing import List, Dict, Any

from app.core.firebase import db
from app.schemas.grade import GradeOut


def get_final_grades_for_assignment(assignment_id: str) -> List[GradeOut]:
    # Traemos TODOS los submissions del assignment
    docs = (
        db.collection("submissions")
        .where("assignment_id", "==", assignment_id)
        .stream()
    )

    by_student: Dict[str, Dict[str, Any]] = {}

    for doc in docs:
        s = doc.to_dict()
        student_id = s["student_id"]
        attempt = s.get("attempt_number", 1)

        if student_id not in by_student or attempt > by_student[student_id].get(
            "attempt_number", 0
        ):
            by_student[student_id] = s

    grades: List[GradeOut] = []
    for student_id, sub in by_student.items():
        score = sub.get("score") or 0.0
        status = "APPROVED" if score >= 51 else "FAILED"

        grades.append(
            GradeOut(
                student_id=student_id,
                assignment_id=assignment_id,
                final_score=score,
                status=status,
            )
        )

    return grades
