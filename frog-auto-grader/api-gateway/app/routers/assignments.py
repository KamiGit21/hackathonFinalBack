from fastapi import APIRouter, Request, Depends, Body
from typing import Any, Dict
from app.services.proxy_service import forward_request
from app.config import settings
from app.deps import current_user
from app.schemas import AuthUser

router = APIRouter(prefix="/assignments", tags=["assignments"])

@router.api_route("/{path:path}", methods=["GET", "POST", "PUT", "PATCH", "DELETE"])
async def proxy_assignments(
    path: str,
    request: Request,
    user: AuthUser = Depends(current_user),
    body: Dict[str, Any] = Body(None)
):
    """
    Forward todas las requests a assignments-service
    """
    return await forward_request(
        service_url=settings.assignments_service_url,
        path=f"/{path}",
        method=request.method,
        headers=dict(request.headers),
        body=body,
        query_params=dict(request.query_params)
    )