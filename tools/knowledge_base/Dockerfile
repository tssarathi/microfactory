FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /bin/

COPY pyproject.toml uv.lock ./
COPY tools/knowledge_base/pyproject.toml tools/knowledge_base/pyproject.toml

RUN uv sync --frozen --package knowledge-base --no-dev

COPY tools/knowledge_base/ tools/knowledge_base/

CMD ["uv", "run", "python", "tools/knowledge_base/server.py"]
