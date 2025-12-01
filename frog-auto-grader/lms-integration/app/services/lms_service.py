from typing import Literal
from app.core.http_client import get_grades_from_assignments
from app.schemas.lms import LmsGradesResponse
from app.schemas.common import Grade


def grades_to_csv(grades: list[Grade]) -> str:
    """
    Convierte la lista de grades en un CSV simple para el LMS (simulado).
    """
    lines = ["student_id,student_name,assignment_id,assignment_name,course_name,final_score,status"]
    for g in grades:
        line = f"{g.student_id},{g.student_name},{g.assignment_id},{g.assignment_name},{g.course_name},{g.final_score},{g.status}"
        lines.append(line)
    return "\n".join(lines)


async def get_lms_grades(assignment_id: int, fmt: Literal["json", "csv"] = "json"):
    raw = await get_grades_from_assignments(assignment_id)

    # Asumimos que assignments-service nos devuelve una lista de dicts tipo Grade
    grades = [Grade(**item) for item in raw]

    if fmt == "json":
        return LmsGradesResponse(
            assignment_id=assignment_id,
            format="json",
            grades=grades
        )
    else:
        csv_content = grades_to_csv(grades)
        # Para CSV probablemente devolvamos solo el texto, el router se encarga del header
        return csv_content
