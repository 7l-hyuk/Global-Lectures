from pydantic import BaseModel


class SttModelConfig(BaseModel):
    language: str
    model: str
    audio_path: str


class SubtitleEntry(BaseModel):
    start: float
    end: float
    text: str
