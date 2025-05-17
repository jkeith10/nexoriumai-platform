FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry

# Install Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

# Copy only dependency declarations first for Docker layer caching
COPY nexoriumai/pyproject.toml ./pyproject.toml

RUN poetry export -f requirements.txt --without-hashes | pip install --no-cache-dir -r /dev/stdin

# Copy application source
COPY nexoriumai ./nexoriumai

CMD ["uvicorn", "nexoriumai.backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"] 