"""Auto-formatted migration."""

from typing import Sequence, Union

import sqlalchemy as sa
from alembic import op

# === Alembic identifiers ===
revision: str = "c3643000fb3d"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Apply migration changes (upgrade DB schema)."""

    # --- users ---
    op.create_table(
        "users",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("username", sa.String(length=150), nullable=False, unique=True),
        sa.Column("password", sa.String(length=255), nullable=False),
        sa.Column("role", sa.String(length=16), nullable=False),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("username", name="uq_users_username"),
    )
    op.create_index("ix_users_id", "users", ["id"])
    op.create_index("ix_users_username", "users", ["username"])

    # --- laws ---
    op.create_table(
        "laws",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("code", sa.String(length=64), nullable=False),
        sa.Column("article", sa.String(length=64), nullable=False),
        sa.Column("title", sa.String(length=255), nullable=False),
        sa.Column("text", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("code", "article", name="uq_laws_code_article"),
    )
    op.create_index("ix_laws_id", "laws", ["id"])
    op.create_index("ix_laws_code", "laws", ["code"])
    op.create_index("ix_laws_article", "laws", ["article"])

    # --- decisions ---
    op.create_table(
        "decisions",
        sa.Column("id", sa.Integer, primary_key=True, nullable=False),
        sa.Column("case_number", sa.String(length=64), nullable=False, unique=True),
        sa.Column("court", sa.String(length=255), nullable=False),
        sa.Column("date_decided", sa.Date, nullable=True),
        sa.Column("summary", sa.Text, nullable=True),
        sa.Column(
            "created_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            nullable=False,
        ),
        sa.Column(
            "updated_at",
            sa.DateTime(timezone=True),
            server_default=sa.func.now(),
            onupdate=sa.func.now(),
            nullable=False,
        ),
        sa.UniqueConstraint("case_number", name="uq_decisions_case_number"),
    )
    op.create_index("ix_decisions_id", "decisions", ["id"])
    op.create_index("ix_decisions_case_number", "decisions", ["case_number"])
    op.create_index("ix_decisions_court", "decisions", ["court"])
    op.create_index("ix_decisions_date_decided", "decisions", ["date_decided"])

    # --- decision_law_link ---
    op.create_table(
        "decision_law_link",
        sa.Column(
            "decision_id",
            sa.Integer,
            sa.ForeignKey("decisions.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.Column(
            "law_id",
            sa.Integer,
            sa.ForeignKey("laws.id", ondelete="CASCADE"),
            primary_key=True,
        ),
        sa.UniqueConstraint("decision_id", "law_id", name="uq_decision_law"),
    )


def downgrade() -> None:
    """Revert migration changes (downgrade DB schema)."""

    op.drop_table("decision_law_link")

    op.drop_index("ix_decisions_date_decided", table_name="decisions")
    op.drop_index("ix_decisions_court", table_name="decisions")
    op.drop_index("ix_decisions_case_number", table_name="decisions")
    op.drop_index("ix_decisions_id", table_name="decisions")
    op.drop_table("decisions")

    op.drop_index("ix_laws_article", table_name="laws")
    op.drop_index("ix_laws_code", table_name="laws")
    op.drop_index("ix_laws_id", table_name="laws")
    op.drop_table("laws")

    op.drop_index("ix_users_username", table_name="users")
    op.drop_index("ix_users_id", table_name="users")
    op.drop_table("users")
