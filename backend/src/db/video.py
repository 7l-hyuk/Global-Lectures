from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from src.db.postgres import Base

class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    length = Column(String(16), nullable=False)
    key = Column(Text)
    creator_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    user = relationship("User", back_populates="videos")
    languages = relationship("VideoLanguage", back_populates="video", cascade="all, delete-orphan")
