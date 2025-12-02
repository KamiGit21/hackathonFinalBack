from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    # Firebase
    FIREBASE_CREDENTIALS_PATH: str = "secrets/firebase-credentials.json"
    
    # Execution settings
    EXECUTION_TIMEOUT: int = 10  # segundos
    MAX_OUTPUT_SIZE: int = 10000  # caracteres
    ALLOWED_LANGUAGES: list = ["python", "java", "javascript"]
    
    # Service URLs
    ASSIGNMENTS_SERVICE_URL: str = "http://assignments-service:8003"
    
    # Security
    MAX_CODE_SIZE: int = 50000  # caracteres
    
    class Config:
        env_file = ".env"
        case_sensitive = True

settings = Settings()