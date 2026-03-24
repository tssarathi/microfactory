FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /bin/

COPY pyproject.toml uv.lock ./
COPY app/pyproject.toml app/pyproject.toml

RUN uv sync --frozen --package app --no-dev

COPY app/app.py app/a2a_client.py ./
COPY app/.chainlit/ .chainlit/
COPY app/chainlit.md ./

CMD ["uv", "run", "--frozen", "--package", "app", "chainlit", "run", "app.py", "--host", "0.0.0.0", "--port", "8005"]
