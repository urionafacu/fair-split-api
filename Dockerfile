FROM python:3.13-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
ENV PORT 8000

WORKDIR /app

RUN apt-get update && apt-get install -y \
  gcc \
  libpq-dev \
  && rm -rf /var/lib/apt/lists/*

COPY requirements.txt /app/
RUN pip install --no-cache-dir -r requirements.txt

COPY . /app/

COPY start.sh /app/
RUN chmod +x /app/start.sh

EXPOSE ${PORT}

CMD ["/app/start.sh"]
