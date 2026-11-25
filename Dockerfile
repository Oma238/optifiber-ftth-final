FROM python:3.12-slim

RUN apt-get update && apt-get install -y --no-install-recommends python3-tk \
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["pytest", "--cov=src/dominio", "--cov=src/infraestructura", "--cov-fail-under=70"]
