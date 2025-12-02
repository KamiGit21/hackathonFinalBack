import httpx
from fastapi import HTTPException, Request
from typing import Any, Dict
from app.config import settings

async def forward_request(
    service_url: str,
    path: str,
    method: str,
    headers: Dict[str, str],
    body: Any = None,
    query_params: Dict[str, str] = None
) -> Dict[str, Any]:
    """
    Reenvía una request al microservicio correspondiente.
    """
    url = f"{service_url}{path}"
    
    # Filtrar headers que no queremos reenviar
    forwarded_headers = {
        k: v for k, v in headers.items()
        if k.lower() not in ["host", "content-length"]
    }

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.request(
                method=method,
                url=url,
                headers=forwarded_headers,
                json=body if body else None,
                params=query_params
            )
            
            # Si la respuesta es JSON, devolverla como dict
            try:
                return response.json()
            except:
                return {"detail": response.text, "status_code": response.status_code}
                
    except httpx.TimeoutException:
        raise HTTPException(status_code=504, detail="Timeout al contactar el servicio")
    except httpx.RequestError as e:
        raise HTTPException(status_code=503, detail=f"Error al contactar el servicio: {str(e)}")