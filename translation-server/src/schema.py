from pydantic import BaseModel


class SubtitleEntry(BaseModel):
    start: float
    end: float
    text: str


class TranslationModelConfig(BaseModel):
    source_lang: str
    target_lang: str
    model: str
    subtitles: list[SubtitleEntry]