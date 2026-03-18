FROM python:3.13-slim
WORKDIR /app
RUN apt-get update && apt-get install -y --no-install-recommends curl && rm -rf /var/lib/apt/lists/*
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /bin/

COPY pyproject.toml uv.lock ./
COPY agents/pyproject.toml agents/pyproject.toml

RUN uv sync --frozen --package agents --no-dev

COPY agents/knowledge/ agents/knowledge/

CMD ["uv", "run", "python", "-m", "agents.knowledge.a2a_server"]
