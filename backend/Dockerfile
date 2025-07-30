FROM 7lhyuku/global-lectures:dubbing_service_base_0.0.0

RUN apt-get update && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic-utf8 sox libsox-fmt-all ffmpeg git

# Work
WORKDIR /app
COPY ./backend .

RUN uv sync --locked

EXPOSE 8000

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
