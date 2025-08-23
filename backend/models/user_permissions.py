from sqlalchemy import BigInteger, Column, ForeignKey

from ..database import Base


class UserPermission(Base):
    __tablename__ = "user_permissions"

    user_id = Column(BigInteger, ForeignKey("users.id"), nullable=False, primary_key=True)
    permission_id = Column(BigInteger, ForeignKey("permissions.id"), nullable=False, primary_key=True)
    granted_by = Column(BigInteger, ForeignKey("users.id"), nullable=False)
