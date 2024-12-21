# Dockerfile
FROM python:3.12-slim

WORKDIR /app

# Copy only the necessary files
COPY requirements.txt .
COPY src/ ./src/

# Install dependencies and clean up in one layer
RUN pip install --no-cache-dir -r requirements.txt && \
    rm -rf requirements.txt

# Create non-root user
RUN useradd -m appuser && \
    chown -R appuser:appuser /app

USER appuser

CMD ["python", "-m", "src.server"]