from sqlalchemy import (TIMESTAMP, BigInteger, Column, ForeignKey, String,
                        Text, func)
from sqlalchemy.orm import relationship

from ..database import Base


class Post(Base):
    __tablename__ = "posts"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    church_id = Column(BigInteger, ForeignKey("church.id"), nullable=False)
    title = Column(String(255), nullable=False)
    media = Column(String(255))  # URL or path to media
    description = Column(Text)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    church = relationship("Church", back_populates="posts")
    author = relationship("User", back_populates="posts")
    comments = relationship("Comment", back_populates="post")
