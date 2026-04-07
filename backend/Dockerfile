FROM python:3.13-slim

# Install uv from the official image (pinned to the version that produced uv.lock)
COPY --from=ghcr.io/astral-sh/uv:0.8.14 /uv /uvx /bin/

WORKDIR /app

# Copy lockfile + manifest first so dep installs cache independently of app code
COPY pyproject.toml uv.lock ./

# Install only production deps (no mypy/pytest/ruff in the prod image)
# --no-install-project defers the local package install until source is present
RUN uv sync --frozen --no-dev --no-install-project

# Copy app code
COPY app/ ./app/
COPY data/ ./data/

# Now install the project itself (source is present for setuptools to find)
RUN uv sync --frozen --no-dev

ENV CHROMA_PERSIST_DIR=/app/chroma_data
ENV KNOWLEDGE_BASE_DIR=/app/data/knowledge_base

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
