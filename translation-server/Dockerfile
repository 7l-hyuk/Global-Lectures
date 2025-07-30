FROM 7lhyuku/global-lectures:dubbing_service_base_0.0.0

RUN apt-get update && apt-get install -y --no-install-recommends mecab libmecab-dev mecab-ipadic-utf8 sox libsox-fmt-all ffmpeg git

# Work
WORKDIR /app
COPY ./translation-server .

RUN uv sync --locked

EXPOSE 8002

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
