from sqlalchemy import Column, Integer, String, DateTime, func, ForeignKey, Text
from sqlalchemy.orm import relationship
from src.models.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    videos = relationship("Video", back_populates="user", cascade="all, delete")


class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(200), nullable=False)
    description = Column(Text, nullable=True)
    length = Column(String(16), nullable=False)
    key = Column(String(32))
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    voice_id = Column(String(32), nullable=True)
    
    user = relationship("User", back_populates="videos")
    languages = relationship("VideoLanguage", back_populates="video", cascade="all, delete-orphan")


class VideoLanguage(Base):
    __tablename__ = "video_language"

    video_id = Column(Integer, ForeignKey("video.id", ondelete="CASCADE"), primary_key=True)
    lang_code = Column(String(10), primary_key=True)
    audio_key = Column(String(32))
    subtitle_key = Column(String(32))

    video = relationship("Video", back_populates="languages")