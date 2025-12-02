FROM python:3.11-slim

# Instalar dependencias del sistema para ejecución de código
RUN apt-get update && apt-get install -y \
    nodejs \
    npm \
    default-jdk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

# Copiar requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código
COPY ./app ./app

# Crear directorio para secrets
RUN mkdir -p secrets

# Exponer puerto
EXPOSE 8003

# Comando para iniciar
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8003", "--reload"]