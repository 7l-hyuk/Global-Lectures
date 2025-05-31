from pydantic import BaseModel


class VideoResponse(BaseModel):
    id: int
    title: str
    length: str
