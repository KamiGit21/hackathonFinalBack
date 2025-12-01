import httpx
from app.core.config import settings


async def get_grades_from_assignments(assignment_id: str):
    """
    Llama a assignments-service:
    GET /api/v1/assignments/{assignment_id}/grades

    Espera una respuesta del tipo:
    {
      "assignment_id": "abc123",
      "items": [ ... GradeOut ... ]
    }
    """
    url = f"{settings.ASSIGNMENTS_SERVICE_URL}/assignments/{assignment_id}/grades"
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url)
        resp.raise_for_status()
        data = resp.json()
        # devolvemos SOLO la lista de items (grades)
        return data.get("items", [])


async def get_audit_logs_from_assignments(year: int):
    """
    Llama a assignments-service:
    GET /api/v1/audit/grades?year=YYYY

    Espera algo como:
    {
      "year": 2025,
      "logs": [ ... GradeAuditLog ... ]
    }
    """
    url = f"{settings.ASSIGNMENTS_SERVICE_URL}/audit/grades"
    params = {"year": year}
    async with httpx.AsyncClient(timeout=10.0) as client:
        resp = await client.get(url, params=params)
        resp.raise_for_status()
        return resp.json()
