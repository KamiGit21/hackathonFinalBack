import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    # Nombre del servicio
    SERVICE_NAME: str = "lms-integration"

    # URL del assignments-service (lo vamos a usar para obtener notas y logs)
    ASSIGNMENTS_SERVICE_URL: str = "http://assignments-service:8005/api/v1"

    # Ambiente (dev, prod, etc.)
    ENV: str = "dev"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
