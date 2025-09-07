FROM python:3.13-slim AS builder

RUN apt-get update && apt-get install -y --no-install-recommends \
    curl \
    build-essential \
    && rm -rf /var/lib/apt/lists/*

RUN pip install poetry

RUN poetry config virtualenvs.create false

WORKDIR /app

ENV PYTHONPATH="/app/src"

COPY pyproject.toml poetry.lock* ./

RUN poetry install --no-interaction --no-root

FROM python:3.13-slim AS runtime

ENV PYTHONPATH="/app/src"

WORKDIR /app

COPY --from=builder /usr/local/lib/python3.13/site-packages /usr/local/lib/python3.13/site-packages
COPY --from=builder /usr/local/bin /usr/local/bin

COPY . .

CMD ["python", "-m", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8080"]
