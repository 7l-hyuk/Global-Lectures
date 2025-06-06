from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    length: str


class VideoUpdate(BaseModel):
    title: str | None
    description: str | None = None


class SubtitleEntry(BaseModel):
    time: float
    end: float
    text: str


class DubAudioRequest(BaseModel):
    video_id: int
    audio_presigned_url: str
    source_lang: str
    target_lang: str
    subtitle: list[SubtitleEntry]
    translation_model: str
    tts_model: str

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )