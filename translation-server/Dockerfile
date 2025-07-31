FROM 7lhyuku/global-lectures:dubbing_service_base_0.0.0

# Work
WORKDIR /app
COPY ./translation-server .

RUN uv sync --locked 
EXPOSE 8002

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8002"]
