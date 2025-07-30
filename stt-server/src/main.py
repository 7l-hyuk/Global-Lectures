import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.schema import SttModelConfig, SubtitleEntry
from src.models.stt import stt_service

app = FastAPI()
app.add_middleware(
   CORSMiddleware,
    allow_origins=["http://backend:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post("/api/v1/stt", response_model=list[SubtitleEntry])
def stt(
    model_config: SttModelConfig
):
    start = time.time()
    stt = stt_service.create_service(
        name="whisperX",
        language=model_config.language
    )
    subtitle = stt.run(audio_path=model_config.audio_path)
    print(f"Processed In {time.time() - start} ms")
    return subtitle
