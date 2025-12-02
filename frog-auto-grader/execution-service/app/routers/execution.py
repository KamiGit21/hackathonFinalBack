from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ExecutionRequest, ExecutionResponse, ExecutionLog
from app.services.execution_service import ExecutionService
from app.repos.execution_repo import ExecutionRepository
from typing import List
import logging

logger = logging.getLogger(__name__)
router = APIRouter()

# Dependencias
def get_execution_service():
    return ExecutionService()

def get_execution_repo():
    return ExecutionRepository()

@router.post("/execute", response_model=ExecutionResponse)
async def execute_code(
    request: ExecutionRequest,
    exec_service: ExecutionService = Depends(get_execution_service),
    exec_repo: ExecutionRepository = Depends(get_execution_repo)
):
    """
    Ejecutar código y calificar con tests
    
    - **submission_id**: ID de la submission
    - **language**: Lenguaje (python, java, javascript)
    - **code**: Código fuente
    - **tests**: Lista de tests con input y expected_output
    """
    try:
        # Validar tamaño del código
        if len(request.code) > 50000:
            raise HTTPException(status_code=400, detail="Código demasiado grande")
        
        # Ejecutar código
        result = exec_service.execute_code(
            submission_id=request.submission_id,
            language=request.language,
            code=request.code,
            tests=request.tests
        )
        
        # Guardar log de ejecución
        log = ExecutionLog(
            submission_id=request.submission_id,
            language=request.language,
            status=result.status,
            score=result.score,
            execution_time=result.execution_time,
            output=str(result.details),
            error=result.details.get('error') if result.status == 'ERROR' else None,
            timestamp=result.timestamp
        )
        
        log_id = exec_repo.save_execution_log(log)
        logger.info(f"Código ejecutado - Submission: {request.submission_id}, Score: {result.score}, Log ID: {log_id}")
        
        return result
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error en ejecución: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs/submission/{submission_id}")
async def get_submission_logs(
    submission_id: int,
    exec_repo: ExecutionRepository = Depends(get_execution_repo)
):
    """Obtener logs de ejecución de una submission"""
    try:
        logger.info(f"Buscando logs para submission_id: {submission_id}")
        logs = exec_repo.get_logs_by_submission(submission_id)
        logger.info(f"Encontrados {len(logs)} logs para submission {submission_id}")
        return {"submission_id": submission_id, "logs": logs, "count": len(logs)}
    except Exception as e:
        logger.error(f"Error obteniendo logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs/recent")
async def get_recent_logs(
    limit: int = 50,
    exec_repo: ExecutionRepository = Depends(get_execution_repo)
):
    """Obtener logs recientes"""
    try:
        logs = exec_repo.get_recent_logs(limit)
        return {"logs": logs, "count": len(logs)}
    except Exception as e:
        logger.error(f"Error obteniendo logs recientes: {e}")
        raise HTTPException(status_code=500, detail=str(e))

@router.get("/logs/all")
async def get_all_logs(
    exec_repo: ExecutionRepository = Depends(get_execution_repo)
):
    """Obtener TODOS los logs (para debugging)"""
    try:
        logs = exec_repo.get_all_logs()
        
        # Agrupar por submission_id para mejor visualización
        by_submission = {}
        for log in logs:
            sid = log.get('submission_id')
            if sid not in by_submission:
                by_submission[sid] = []
            by_submission[sid].append(log)
        
        return {
            "total_logs": len(logs),
            "logs": logs,
            "by_submission": by_submission,
            "submission_ids": list(by_submission.keys())
        }
    except Exception as e:
        logger.error(f"Error obteniendo todos los logs: {e}")
        raise HTTPException(status_code=500, detail=str(e))