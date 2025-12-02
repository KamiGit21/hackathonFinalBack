import firebase_admin
from firebase_admin import credentials, firestore
from app.config import settings
import logging
import os

logger = logging.getLogger(__name__)

_db_client = None

def initialize_firebase():
    """Inicializar Firebase Admin SDK"""
    global _db_client
    
    try:
        if not firebase_admin._apps:
            # Verificar si existe el archivo de credenciales
            if os.path.exists(settings.FIREBASE_CREDENTIALS_PATH):
                cred = credentials.Certificate(settings.FIREBASE_CREDENTIALS_PATH)
                firebase_admin.initialize_app(cred)
                logger.info("Firebase initialized successfully")
            else:
                logger.warning(f"Firebase credentials not found at {settings.FIREBASE_CREDENTIALS_PATH}")
                logger.warning("Firebase will not be available. Running in mock mode.")
                return None
        
        _db_client = firestore.client()
        return _db_client
    except Exception as e:
        logger.error(f"Error initializing Firebase: {e}")
        logger.warning("Running without Firebase persistence")
        return None

def get_firestore_client():
    """Obtener cliente de Firestore"""
    global _db_client
    
    if _db_client is None:
        _db_client = initialize_firebase()
    
    return _db_client