FROM python:3.11-slim

ENV POETRY_VERSION=1.8.2 \
    POETRY_HOME=/opt/poetry

# Install Poetry
RUN pip install --no-cache-dir "poetry==${POETRY_VERSION}"

WORKDIR /app

# Copy only dependency declarations first for Docker layer caching
COPY nexoriumai/pyproject.toml ./pyproject.toml

# Install dependencies using poetry install instead of export
RUN poetry install --no-root

# Copy application source
COPY nexoriumai ./nexoriumai

CMD ["poetry", "run", "uvicorn", "nexoriumai.backend.api.main:app", "--host", "0.0.0.0", "--port", "8000"]