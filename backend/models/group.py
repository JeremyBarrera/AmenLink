from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, String, func
from sqlalchemy.orm import relationship

from ..database import Base


class Group(Base):
    __tablename__ = "groups"

    id = Column(BigInteger, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)
    created_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    created_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    creator = relationship("User", back_populates="groups_created")
    members = relationship("GroupMember", back_populates="group")
