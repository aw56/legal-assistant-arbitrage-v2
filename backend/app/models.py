from datetime import datetime

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String, Text
from sqlalchemy.dialects.postgresql import ENUM
from sqlalchemy.orm import relationship

from backend.app.core.enums import UserRole
from backend.app.database import Base


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    email = Column(String, unique=True, index=True, nullable=False)
    password_hash = Column(String, nullable=False)  # ✅ храним хеш, а не пароль
    role = Column(
        ENUM(UserRole, name="userrole_enum"), default=UserRole.client, nullable=False
    )
    created_at = Column(DateTime, default=datetime.utcnow)

    decisions = relationship("Decision", back_populates="user")


class Law(Base):
    __tablename__ = "laws"

    id = Column(Integer, primary_key=True, index=True)
    code = Column(String, nullable=False)
    article = Column(String, nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)

    decisions = relationship("Decision", back_populates="law")


class Decision(Base):
    __tablename__ = "decisions"

    id = Column(Integer, primary_key=True, index=True)
    case_number = Column(String, unique=True, index=True, nullable=False)
    court = Column(String, nullable=False)
    date_decided = Column(DateTime, nullable=False)
    summary = Column(Text, nullable=True)

    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(
        DateTime, default=datetime.utcnow, onupdate=datetime.utcnow
    )  # ✅ новое поле

    law_id = Column(Integer, ForeignKey("laws.id"), nullable=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)

    law = relationship("Law", back_populates="decisions")
    user = relationship("User", back_populates="decisions")
