FROM 7lhyuku/global-lectures:dubbing_service_base_0.0.0

# Work
WORKDIR /app
COPY ./tts-server .

RUN uv sync --locked 
EXPOSE 8003

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8003"]
