from datetime import datetime
from pydantic import BaseModel, ConfigDict


class VideoResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    length: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class VideoUpdate(BaseModel):
    title: str | None
    description: str | None = None

    model_config = ConfigDict(
        json_schema_extra={
            "example": {
                "title": "My Lecture",
                "description": "Updated description...",
            }
        }
    )


class SubtitleEntry(BaseModel):
    time: float
    end: float
    text: str
