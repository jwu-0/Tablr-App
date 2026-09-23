FROM python:3.12-slim AS base

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_NO_CACHE_DIR=1

WORKDIR /srv

# Install dependencies first so the layer caches across code changes.
COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install .

COPY app ./app
COPY scripts ./scripts

# Never bake secrets into the image — they arrive as environment variables.
EXPOSE 8000

# Run as a non-root user.
RUN useradd --create-home --uid 10001 tablr
USER tablr

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
