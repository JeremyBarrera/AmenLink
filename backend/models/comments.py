from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, Text, func
from sqlalchemy.orm import relationship

from ..database import Base


class Comment(Base):
    __tablename__ = "comments"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    post_id = Column(BigInteger, ForeignKey("posts.id"), nullable=False)
    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    comment = Column(Text, nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    post = relationship("Post", back_populates="comments")
    author = relationship("User", back_populates="comments")
