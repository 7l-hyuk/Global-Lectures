from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship
from src.db.postgres import Base


class VideoLanguage(Base):
    __tablename__ = "video_language"

    video_id = Column(Integer, ForeignKey("video.id", ondelete="CASCADE"), primary_key=True)
    lang_code = Column(String(10), primary_key=True)

    audio_key = Column(Text)
    subtitle_key = Column(Text)

    video = relationship("Video", back_populates="languages")
