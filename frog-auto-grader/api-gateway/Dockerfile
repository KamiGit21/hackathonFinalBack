FROM python:3.11-slim

# Establecer directorio de trabajo
WORKDIR /app

# Instalar dependencias del sistema necesarias para algunas librerías de Python
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copiar requirements primero (para aprovechar cache de Docker)
COPY requirements.txt .

# Instalar dependencias de Python
RUN pip install --no-cache-dir -r requirements.txt

# Copiar el código de la aplicación
COPY ./app /app/app

# Copiar la carpeta secrets (credenciales Firebase)
COPY ./secrets /app/secrets

# Exponer el puerto 8000
EXPOSE 8000

# Variables de entorno por defecto (se sobreescriben con .env)
ENV PYTHONUNBUFFERED=1
ENV PORT=8000

# Comando para ejecutar la aplicación
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]