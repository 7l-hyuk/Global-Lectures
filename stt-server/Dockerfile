FROM 7lhyuku/global-lectures:dubbing_service_base_0.0.0

# Work
WORKDIR /app
COPY ./stt-server .

RUN uv sync --locked 
EXPOSE 8001      

CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8001"]
