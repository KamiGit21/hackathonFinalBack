from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.routers import execution
from app.config import settings
from app.firebase import initialize_firebase
import logging

# Configurar logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(
    title="Execution & Grading Service",
    description="Servicio para ejecutar y calificar código de estudiantes",
    version="1.0.0"
)

# CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Inicializar Firebase al arrancar"""
    logger.info("Starting Execution & Grading Service...")
    try:
        initialize_firebase()
        logger.info("Firebase initialization completed")
    except Exception as e:
        logger.warning(f"Firebase initialization failed: {e}")
        logger.warning("Service will run without Firebase persistence")

# Incluir routers
app.include_router(execution.router, prefix="/api/v1", tags=["execution"])

@app.get("/")
async def root():
    return {
        "service": "Execution & Grading Service",
        "status": "running",
        "version": "1.0.0"
    }

@app.get("/health")
async def health_check():
    return {"status": "healthy"}

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8003)