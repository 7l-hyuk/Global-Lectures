FROM python:3.11-slim-bookworm
COPY --from=ghcr.io/astral-sh/uv:latest /uv /uvx /bin/

RUN apt-get update && apt-get install -y --no-install-recommends sox ffmpeg git\
    && rm -rf /var/lib/apt/lists/*

WORKDIR /app
COPY ./backend .

RUN uv sync
RUN uv pip install TTS
RUN uv pip install hf_xet

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
