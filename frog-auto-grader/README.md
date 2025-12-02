# Frog Auto-Grader - Sistema de Calificación Automática

Sistema de microservicios para la calificación automática de tareas de programación universitarias.

## 🏗️ Arquitectura

- **API Gateway** (Puerto 8000): Punto de entrada único, autenticación OAuth + Firebase
- **Assignments Service** (Puerto 8002): Gestión de tareas, entregas, criterios y auditoría
- **Execution Service** (Puerto 8003): Ejecución de código en sandbox y calificación
- **Plagiarism Service** (Puerto 8004): Detección de plagio + integración TurnItIn
- **LMS Integration** (Puerto 8005): Sincronización con sistemas LMS (Moodle, Canvas, etc.)

## 🚀 Inicio Rápido

### Prerrequisitos

- Docker y Docker Compose instalados
- Credenciales de Firebase en `api-gateway/secrets/auth-service-credentials.json`

### Levantar todos los servicios
```bash
docker-compose up --build
```

### Acceder a la documentación

- API Gateway: http://localhost:8000/docs
- Assignments Service: http://localhost:8002/docs
- Execution Service: http://localhost:8003/docs
- Plagiarism Service: http://localhost:8004/docs
- LMS Integration: http://localhost:8005/docs

## 🔐 Autenticación

1. Inicia sesión con Google: `GET http://localhost:8000/auth/google/login`
2. Usa el token JWT en el header: `Authorization: Bearer <token>`

## 📦 Proyecto Firebase

- **Nombre**: API-GETAWAY
- **ID**: api-getaway-70355
- **Número**: 421154360368

## 🛠️ Desarrollo

Cada microservicio es independiente:
```bash
cd api-gateway
pip install -r requirements.txt
uvicorn app.main:app --reload --port 8000
```

## 📝 Variables de Entorno

Cada servicio tiene su propio `.env`. Ver archivos `.env.example` en cada carpeta.

## 🧪 Testing
```bash
# Healthcheck de todos los servicios
curl http://localhost:8000/health
curl http://localhost:8002/health
curl http://localhost:8003/health
curl http://localhost:8004/health
curl http://localhost:8005/health
```

## 👥 Roles de Usuario

- **ADMIN**: Acceso completo al sistema
- **PROFESSOR**: Crear tareas, ver entregas, calificar
- **STUDENT**: Enviar tareas, ver sus calificaciones

## 📄 Licencia

Frog Software Ltda. - Sistema Universitario de Calificación Automática
```

---

## **6. .gitignore (raíz del proyecto)**
```
# Python
__pycache__/
*.py[cod]
*$py.class
*.so
.Python
env/
venv/
ENV/
.venv

# Secrets y credenciales
**/secrets/**
!**/secrets/.gitkeep
**/*.json
!package*.json

# Environment
.env
.env.local
**/.env
**/.env.local

# IDE
.vscode/
.idea/
*.swp
*.swo

# OS
.DS_Store
Thumbs.db

# Docker
*.log
docker-compose.override.yml

# Firebase
.firebase/
firebase-debug.log