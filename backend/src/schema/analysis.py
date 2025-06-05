from pydantic import BaseModel


class Subtitle(BaseModel):
    text: str
    start: float
    end: float