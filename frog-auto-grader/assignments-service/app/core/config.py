from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "assignments-service"
    FIREBASE_CREDENTIALS: str = "firebase-key.json"  # ruta al json

    ENV: str = "dev"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
