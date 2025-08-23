from sqlalchemy import TIMESTAMP, BigInteger, Column, Integer, String, func
from sqlalchemy.orm import relationship

from ..database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    username = Column(String(50), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    email = Column(String(100), unique=True)
    phone_number = Column(String(20))
    age = Column(Integer)
    role = Column(String(255))  # user or admin
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    churches = relationship("Church", back_populates="creator")
    posts = relationship("Post", back_populates="author")
    comments = relationship("Comment", back_populates="author")
    groups_created = relationship("Group", back_populates="creator")
    memberships = relationship("GroupMember", back_populates="user")
