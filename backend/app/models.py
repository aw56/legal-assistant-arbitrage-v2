from __future__ import annotations

from datetime import date, datetime
from typing import List, Optional

from sqlalchemy import Column, Date, DateTime
from sqlalchemy import Enum as SAEnum
from sqlalchemy import (
    ForeignKey,
    Index,
    Integer,
    String,
    Table,
    Text,
    UniqueConstraint,
    func,
)
from sqlalchemy.orm import Mapped, mapped_column, relationship

from backend.app.database import Base
from backend.app.schemas.user import UserRole  # ✅ используем общий Enum

# --- Ассоциация Решение ↔ Норма (многие-ко-многим) ----------------------------

decision_law_link = Table(
    "decision_law_link",
    Base.metadata,
    Column(
        "decision_id",
        Integer,
        ForeignKey("decisions.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    Column(
        "law_id",
        Integer,
        ForeignKey("laws.id", ondelete="CASCADE"),
        primary_key=True,
    ),
    UniqueConstraint("decision_id", "law_id", name="uq_decision_law"),
)


# --- Модели --------------------------------------------------------------------


class User(Base):
    __tablename__ = "users"
    __table_args__ = (
        UniqueConstraint("username", name="uq_users_username"),
        Index("ix_users_username", "username"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    username: Mapped[str] = mapped_column(String(150), nullable=False, unique=True)
    password: Mapped[str] = mapped_column(String(255), nullable=False)

    role: Mapped[UserRole] = mapped_column(
        SAEnum(UserRole, native_enum=False, length=16),  # хранится как VARCHAR
        default=UserRole.client,
        nullable=False,
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<User id={self.id} username={self.username!r} role={self.role.value}>"


class Law(Base):
    __tablename__ = "laws"
    __table_args__ = (
        UniqueConstraint("code", "article", name="uq_laws_code_article"),
        Index("ix_laws_code", "code"),
        Index("ix_laws_article", "article"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    code: Mapped[str] = mapped_column(String(64), nullable=False)  # например: "АПК РФ"
    article: Mapped[str] = mapped_column(
        String(64), nullable=False
    )  # например: "ст. 125"
    title: Mapped[str] = mapped_column(
        String(255), nullable=False
    )  # краткое название статьи
    text: Mapped[str | None] = mapped_column(Text, nullable=True)

    # связи
    decisions: Mapped[List["Decision"]] = relationship(
        secondary=decision_law_link,
        back_populates="laws",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Law id={self.id} {self.code} {self.article}>"


class Decision(Base):
    __tablename__ = "decisions"
    __table_args__ = (
        UniqueConstraint("case_number", name="uq_decisions_case_number"),
        Index("ix_decisions_case_number", "case_number"),
        Index("ix_decisions_court", "court"),
        Index("ix_decisions_date_decided", "date_decided"),
    )

    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    case_number: Mapped[str] = mapped_column(
        String(64), nullable=False, unique=True
    )  # № дела
    court: Mapped[str] = mapped_column(String(255), nullable=False)  # суд
    date_decided: Mapped[Optional[date]] = mapped_column(
        Date, nullable=True
    )  # дата решения
    summary: Mapped[Optional[str]] = mapped_column(
        Text, nullable=True
    )  # короткая выжимка

    # связи
    laws: Mapped[List[Law]] = relationship(
        secondary=decision_law_link,
        back_populates="decisions",
        lazy="selectin",
    )

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True), server_default=func.now(), nullable=False
    )
    updated_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        server_default=func.now(),
        onupdate=func.now(),
        nullable=False,
    )

    def __repr__(self) -> str:
        return f"<Decision id={self.id} case={self.case_number!r}>"
