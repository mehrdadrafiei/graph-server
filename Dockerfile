FROM python:3.12-slim

WORKDIR /app

COPY requirements.txt .
COPY src/ ./src/
COPY .env .

RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt

RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

ENV PYTHONPATH=/app/src

CMD ["python", "-m", "graph_server.server"]