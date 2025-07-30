import time
import os
from io import BytesIO

from uuid import uuid4
from fastapi import FastAPI, UploadFile, File, Form, Body
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware

from src.models.tts import tts_service

tts_model = None

app = FastAPI()
app.add_middleware(
   CORSMiddleware,
    allow_origins=["http://backend:8000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class VoiceIdNotFoundError(Exception):
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)


def iter_file_chunk(file: BytesIO, chunk_size: int=1024*1024):
    while True:
        data = file.read(chunk_size)
        if not data:
            break
        yield data


@app.post("/api/v1/voice-id")
async def get_voice_id(speaker_wav: UploadFile = File(...)):
    print("START: save file")
    os.makedirs("./ref", exist_ok=True)
    speaker_id = uuid4()
    file_path = f"./ref/{speaker_id}.wav"

    with open(file_path, "wb") as wav:
        content = await speaker_wav.read()
        wav.write(content)
    print("END: save file")
    return {"voice_id": speaker_id}


@app.post("/api/v1/tts")
def subtitle_translate(
    target_lang: str = Form(...),
    model: str = Form(...),
    text: str = Form(...),
    voice_id: str = Form(...), 
) -> StreamingResponse:
    global tts_model
    print("START: tts")
    start = time.time()
    speaker_wav = f"./ref/{voice_id}.wav"
    if not os.path.exists(speaker_wav):
        print(speaker_wav)
        raise VoiceIdNotFoundError(f"Voide id {voice_id} dose not exist. Generate voice id before tts.")

    if not tts_model:
        print("Init tts model")
        tts_model = tts_service.create_service(
            name=model,
            target_lang=target_lang,
        )
    buffer, _ = tts_model.run(
        text=text,
        speaker_wav=speaker_wav
    )
    print(f"Processed In {time.time() - start} s")
    print("END: tts")
    return StreamingResponse(
        iter_file_chunk(buffer),
        media_type="audio/wav"
    )


@app.delete("/api/v1/voice-id")
def get_voice_id(voice_id: str):
    os.remove(f"./ref/{voice_id}.wav")
    return f"Delete {voice_id}"
