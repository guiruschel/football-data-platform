FROM python:3.11-slim

ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1 \
    PYTHONPATH=/workspace/ingestion/src

WORKDIR /workspace

RUN apt-get update \
    && apt-get install -y --no-install-recommends build-essential libpq-dev \
    && rm -rf /var/lib/apt/lists/*

RUN pip install --no-cache-dir pandas requests psycopg2-binary pytest

COPY ingestion/src /workspace/ingestion/src
COPY ingestion/tests /workspace/ingestion/tests

CMD ["python", "-m", "football_data_platform.cli"]
