FROM python:3.9-slim

WORKDIR /app

# Instalar dependencias del sistema
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements y instalar dependencias Python
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copiar código de la aplicación
COPY app/ ./app/
COPY run.py .

# Crear directorio de logs
RUN mkdir -p logs

# Exponer puerto
EXPOSE 5000

# Comando para ejecutar la aplicación
CMD ["python", "run.py"] 