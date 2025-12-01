from typing import Literal

from app.core.http_client import get_grades_from_assignments
from app.schemas.lms import LmsGradesResponse
from app.schemas.common import Grade


def grades_to_csv(grades: list[Grade]) -> str:
    """
    Convierte la lista de grades en un CSV simple para el LMS legacy.
    """
    header = "student_id,assignment_id,final_score,status"
    lines = [header]

    for g in grades:
        line = f"{g.student_id},{g.assignment_id},{g.final_score},{g.status}"
        lines.append(line)

    return "\n".join(lines)


async def get_lms_grades(
    assignment_id: str,
    fmt: Literal["json", "csv"] = "json",
):
    raw_items = await get_grades_from_assignments(assignment_id)
    grades = [Grade(**item) for item in raw_items]

    if fmt == "json":
        return LmsGradesResponse(
            assignment_id=assignment_id,
            format="json",
            grades=grades,
        )

    # fmt == "csv"
    csv_content = grades_to_csv(grades)
    return csv_content
