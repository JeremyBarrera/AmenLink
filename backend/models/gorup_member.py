from sqlalchemy import TIMESTAMP, BigInteger, Column, ForeignKey, func
from sqlalchemy.orm import relationship

from ..database import Base


class GroupMember(Base):
    __tablename__ = "group_members"

    group_id = Column(BigInteger, ForeignKey("groups.id"), primary_key=True)
    user_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    added_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
    added_at = Column(TIMESTAMP, server_default=func.now())

    # Relationships
    group = relationship("Group", back_populates="members")
    user = relationship("User", back_populates="memberships")
