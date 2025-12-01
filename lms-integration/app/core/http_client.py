import httpx
from app.core.config import settings


async def get_grades_from_assignments(assignment_id: int):
    """
    Llama al assignments-service para obtener las notas de una asignación.
    Esta función la usaremos en el LMS service.
    """
    url = f"{settings.ASSIGNMENTS_SERVICE_URL}/assignments/{assignment_id}/grades"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        return resp.json()


async def get_audit_logs_from_assignments(year: int):
    """
    Llama al assignments-service para obtener los logs de auditoría de notas de un año.
    """
    url = f"{settings.ASSIGNMENTS_SERVICE_URL}/audit/grades"
    params = {"year": year}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
