from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.sessions import SessionMiddleware

from app.config import settings
from app.firebase import init_firebase
from app.routers import auth
from app.routers import assignments
from app.routers import submissions
from app.routers import lms

@asynccontextmanager
async def lifespan(app: FastAPI):
    """
    Ciclo de vida de la aplicación.
    Se ejecuta al inicio y al apagar el servidor.
    """
    # Startup: Inicializar Firebase
    try:
        init_firebase()
        print("[INFO] ✅ Firebase inicializado correctamente")
    except Exception as e:
        print(f"[ERROR] ❌ Firebase init failed: {e}")
    
    yield
    
    # Shutdown: Limpieza si es necesaria
    print("[INFO] 🛑 API Gateway cerrándose...")

app = FastAPI(
    title="Frog Auto-Grader API Gateway",
    description="Punto de entrada único para todos los microservicios del sistema de calificación automática",
    version="1.0.0",
    lifespan=lifespan,
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# ══════════════════════════════════════════════════════════════════════════════
# MIDDLEWARE
# ══════════════════════════════════════════════════════════════════════════════

# Middleware de sesión (necesario para OAuth)
app.add_middleware(
    SessionMiddleware,
    secret_key=settings.session_secret,
    same_site="lax",
    https_only=False,  # Cambiar a True en producción con HTTPS
)

# CORS (permitir acceso desde el frontend)
allowed_origins = settings.cors_origins or ["http://localhost:3000"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=allowed_origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
    expose_headers=["*"]
)

# ══════════════════════════════════════════════════════════════════════════════
# ROUTERS
# ══════════════════════════════════════════════════════════════════════════════

# Autenticación (OAuth + Firebase)
app.include_router(auth.router)

# Proxy a microservicios
app.include_router(assignments.router)
app.include_router(submissions.router)
app.include_router(lms.router)

# ══════════════════════════════════════════════════════════════════════════════
# ENDPOINTS BASE
# ══════════════════════════════════════════════════════════════════════════════

@app.get("/")
def root():
    """
    Endpoint raíz - Información del API Gateway
    """
    return {
        "service": "Frog Auto-Grader API Gateway",
        "version": "1.0.0",
        "status": "running",
        "description": "Sistema de calificación automática de tareas de programación",
        "endpoints": {
            "auth": "/auth/google/login",
            "docs": "/docs",
            "health": "/health",
            "me": "/auth/me"
        },
        "microservices": {
            "assignments": settings.assignments_service_url,
            "execution": settings.execution_service_url,
            "plagiarism": settings.plagiarism_service_url,
            "lms": settings.lms_service_url
        }
    }


@app.get("/health")
def health():
    """
    Health check - Verificar que el servicio está funcionando
    """
    return {
        "status": "ok",
        "service": "api-gateway",
        "port": 8000,
        "firebase_project": settings.firebase_project_id
    }


@app.get("/info")
def info():
    """
    Información detallada del sistema
    """
    return {
        "project": "Frog Auto-Grader",
        "gateway_version": "1.0.0",
        "firebase_project_id": settings.firebase_project_id,
        "available_services": {
            "assignments": f"{settings.assignments_service_url}",
            "execution": f"{settings.execution_service_url}",
            "plagiarism": f"{settings.plagiarism_service_url}",
            "lms": f"{settings.lms_service_url}"
        },
        "authentication": {
            "provider": "Google OAuth + Firebase",
            "login_url": "/auth/google/login",
            "token_type": "JWT Bearer"
        },
        "roles": ["ADMIN", "PROFESSOR", "STUDENT"]
    }