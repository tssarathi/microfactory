FROM python:3.13-slim
WORKDIR /app
COPY --from=ghcr.io/astral-sh/uv:0.10.4 /uv /bin/

COPY pyproject.toml uv.lock ./
COPY agents/pyproject.toml agents/pyproject.toml

RUN uv sync --frozen --package agents --no-dev

COPY agents/field_service/ agents/field_service/

CMD ["uv", "run", "python", "-m", "agents.field_service.a2a_server"]
