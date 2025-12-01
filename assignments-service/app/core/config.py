import os
from pydantic import BaseSettings


class Settings(BaseSettings):
    SERVICE_NAME: str = "assignments-service"

    # DATABASE_URL formato:
    # postgresql+psycopg2://user:password@db-host:5432/dbname
    DATABASE_URL: str = "postgresql+psycopg2://user:password@db:5432/assignments_db"

    ENV: str = "dev"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
