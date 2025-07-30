FROM python:3.11-slim-bookworm

RUN apt-get update && apt-get install -y --no-install-recommends curl ca-certificates mecab libmecab-dev mecab-ipadic-utf8 sox libsox-fmt-all ffmpeg git\
    && rm -rf /var/lib/apt/lists/*

# Download the latest installer
ADD https://astral.sh/uv/install.sh /uv-installer.sh

# Run the installer then remove it
RUN sh /uv-installer.sh && rm /uv-installer.sh

# Ensure the installed binary is on the `PATH`
ENV PATH="/root/.local/bin/:$PATH"

# Work
WORKDIR /app
COPY ./backend .

RUN uv sync --locked

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "src.main:app", "--port", "8000"]
