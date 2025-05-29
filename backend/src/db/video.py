from sqlalchemy import Column, Integer, String, Text, Time, DateTime, ForeignKey, func
from sqlalchemy.orm import relationship

from src.db.postgres import Base

class Video(Base):
    __tablename__ = "video"

    id = Column(Integer, primary_key=True, index=True)

    title = Column(String(200), nullable=False)
    length = Column(Time, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    key = Column(Text)

    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), nullable=False)

    user = relationship("User", back_populates="videos")
    languages = relationship("VideoLanguage", back_populates="video", cascade="all, delete-orphan")
