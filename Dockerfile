FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app

# Instalar dependencias del sistema si son necesarias
RUN apt-get update && apt-get install -y \
  gcc \
  && rm -rf /var/lib/apt/lists/*

# Copiar requirements e instalar dependencias
COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

# Instalar gunicorn
RUN pip install gunicorn

# Copiar el proyecto
COPY . /app/

# Script de inicio
COPY start.sh /app/
RUN chmod +x /app/start.sh

# Puerto que usará Railway
EXPOSE ${PORT}

# Comando para iniciar la aplicación
CMD ["/app/start.sh"]
