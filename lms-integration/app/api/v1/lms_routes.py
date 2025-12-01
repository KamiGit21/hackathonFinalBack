from fastapi import APIRouter, Query
from fastapi.responses import PlainTextResponse
from typing import Literal

from app.services.lms_service import get_lms_grades
from app.schemas.lms import LmsGradesResponse
from app.schemas.lms import LmsSyncResult

router = APIRouter(
    prefix="/lms",
    tags=["lms"]
)


@router.get("/grades", response_model=LmsGradesResponse)
async def get_grades_for_lms(
    assignment_id: int = Query(..., description="ID de la asignación"),
):
    """
    Devuelve las calificaciones de una asignación en formato JSON,
    simulando el formato que consumiría el LMS.
    """
    result = await get_lms_grades(assignment_id, fmt="json")
    return result


@router.get(
    "/grades.csv",
    response_class=PlainTextResponse,
    summary="Exportar calificaciones en CSV para LMS"
)
async def get_grades_for_lms_csv(
    assignment_id: int = Query(..., description="ID de la asignación"),
):
    """
    Devuelve las calificaciones en formato CSV para el LMS legacy.
    """
    csv_content = await get_lms_grades(assignment_id, fmt="csv")
    return PlainTextResponse(
        content=csv_content,
        media_type="text/csv",
        headers={
            "Content-Disposition": f'attachment; filename="assignment_{assignment_id}_grades.csv"'
        },
    )


@router.post("/sync", response_model=LmsSyncResult)
async def sync_with_lms(assignment_id: int):
    """
    Simula el envío de las calificaciones al LMS (mainframe).
    Por ahora solo devuelve un mensaje de éxito.
    """
    # Aquí podrías reutilizar get_lms_grades y hacer un "fake send"
    return LmsSyncResult(
        assignment_id=assignment_id,
        sent_to_lms=True,
        message="Calificaciones preparadas y 'enviadas' al LMS legacy (simulado)."
    )
