FROM python:3.13-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /bin/

COPY pyproject.toml uv.lock ./
COPY tools/database/pyproject.toml tools/database/pyproject.toml

RUN uv sync --frozen --package mcp-database --no-dev

COPY tools/database/ tools/database/

CMD ["uv", "run", "python", "tools/database/server.py"]
