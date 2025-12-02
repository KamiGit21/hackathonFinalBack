from datetime import datetime
from typing import List, Dict, Any, Optional
from app.firebase import get_firestore_client
from app.schemas import ExecutionLog
import logging

logger = logging.getLogger(__name__)

class ExecutionRepository:
    
    def __init__(self):
        self.db = get_firestore_client()
        self.collection = "execution_logs"
    
    def save_execution_log(self, log: ExecutionLog) -> str:
        """Guardar log de ejecución en Firestore"""
        try:
            # Si Firebase no está disponible, solo log
            if self.db is None:
                logger.warning("Firebase not available. Log not persisted.")
                logger.info(f"Execution log (not saved): submission_id={log.submission_id}, score={log.score}")
                return "mock-id"
            
            log_dict = log.model_dump()
            log_dict['timestamp'] = datetime.utcnow()
            
            doc_ref = self.db.collection(self.collection).document()
            doc_ref.set(log_dict)
            
            logger.info(f"Log de ejecución guardado: {doc_ref.id} para submission {log.submission_id}")
            return doc_ref.id
            
        except Exception as e:
            logger.error(f"Error guardando log de ejecución: {e}")
            logger.info(f"Continuing without persistence for submission {log.submission_id}")
            return "error-id"
    
    def get_execution_log(self, log_id: str) -> Optional[Dict[str, Any]]:
        """Obtener log de ejecución por ID"""
        try:
            if self.db is None:
                logger.warning("Firebase not available")
                return None
                
            doc_ref = self.db.collection(self.collection).document(log_id)
            doc = doc_ref.get()
            
            if doc.exists:
                return doc.to_dict()
            return None
            
        except Exception as e:
            logger.error(f"Error obteniendo log de ejecución: {e}")
            return None
    
    def get_logs_by_submission(self, submission_id: int) -> List[Dict[str, Any]]:
        """Obtener todos los logs de una submission"""
        try:
            if self.db is None:
                logger.warning("Firebase not available")
                return []
            
            # Solución: No usar order_by con where para evitar necesidad de índice compuesto
            docs = self.db.collection(self.collection)\
                .where('submission_id', '==', submission_id)\
                .stream()
            
            # Ordenar en memoria
            results = [doc.to_dict() for doc in docs]
            results.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            
            logger.info(f"Found {len(results)} logs for submission {submission_id}")
            return results
            
        except Exception as e:
            logger.error(f"Error obteniendo logs por submission: {e}")
            logger.exception(e)  # Log completo del error
            return []
    
    def get_recent_logs(self, limit: int = 100) -> List[Dict[str, Any]]:
        """Obtener logs recientes"""
        try:
            if self.db is None:
                logger.warning("Firebase not available")
                return []
            
            # Obtener todos y ordenar en memoria (más simple para evitar índices)
            docs = self.db.collection(self.collection)\
                .limit(limit * 2)\
                .stream()
            
            results = [doc.to_dict() for doc in docs]
            
            # Ordenar por timestamp en memoria
            results.sort(key=lambda x: x.get('timestamp', datetime.min), reverse=True)
            
            # Aplicar límite después de ordenar
            return results[:limit]
            
        except Exception as e:
            logger.error(f"Error obteniendo logs recientes: {e}")
            logger.exception(e)
            return []
    
    def get_all_logs(self) -> List[Dict[str, Any]]:
        """Obtener TODOS los logs (útil para debugging)"""
        try:
            if self.db is None:
                logger.warning("Firebase not available")
                return []
            
            docs = self.db.collection(self.collection).stream()
            results = [doc.to_dict() for doc in docs]
            
            logger.info(f"Total logs in database: {len(results)}")
            return results
            
        except Exception as e:
            logger.error(f"Error obteniendo todos los logs: {e}")
            return []