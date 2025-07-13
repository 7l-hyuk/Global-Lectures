from pydantic import BaseModel, ConfigDict


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    length: str

    model_config = ConfigDict(
        from_attributes=True
    )


class VideoUpdate(BaseModel):
    title: str | None
    description: str | None = None


class SubtitleEntry(BaseModel):
    time: float
    end: float
    text: str
