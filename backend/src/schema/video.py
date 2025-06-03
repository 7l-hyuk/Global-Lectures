from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class VideoResponse(BaseModel):
    id: int
    title: str
    length: str


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

    model_config = ConfigDict(
        alias_generator=to_camel,
        populate_by_name=True
    )