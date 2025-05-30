from pydantic import BaseModel
from datetime import timedelta


class VideoResponse(BaseModel):
    id: int
    title: str
    length: timedelta
    url: str
