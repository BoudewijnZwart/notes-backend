FROM docker.io/python:3.13-alpine

# Install uv
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

WORKDIR /app

# compile to bytecode for speed
ENV UV_COMPILE_BYTECODE=1

# don't buffer stdout and stderror
ENV PYTHONUNBUFFERED=1

ENV PATH="/app/.venv/bin:$PATH"

# Copy the project into the image
COPY . /app

# install project
RUN uv sync --frozen --no-dev

# just for documentation, fastapi by default serves on port 8000
EXPOSE 8000

CMD ["fastapi", "run", "app/main.py"]
