from sqlalchemy import Column, Integer, String, DateTime, func
from sqlalchemy.orm import relationship
from src.db.postgres import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)

    username = Column(String(50), unique=True, index=True, nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password = Column(String(256), nullable=False)

    created_at = Column(DateTime(timezone=True), server_default=func.now())

    videos = relationship("Video", back_populates="user", cascade="all, delete")
