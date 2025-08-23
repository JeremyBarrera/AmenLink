from sqlalchemy import BigInteger, Column, ForeignKey

from ..database import Base


class Admin(Base):
    __tablename__ = "admin"

    admin_id = Column(BigInteger, ForeignKey("users.id"), primary_key=True)
    church_id = Column(BigInteger, ForeignKey("church.id"), primary_key=True)
