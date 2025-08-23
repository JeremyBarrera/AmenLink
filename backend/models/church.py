from sqlalchemy import BigInteger, Column, ForeignKey, String
from sqlalchemy.orm import relationship

from ..database import Base


class Church(Base):
    __tablename__ = "church"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    location = Column(String(255), nullable=False)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)

    # Relationships
    creator = relationship("User", back_populates="churches")
    posts = relationship("Post", back_populates="church")
    admins = relationship("Admin", back_populates="church")
