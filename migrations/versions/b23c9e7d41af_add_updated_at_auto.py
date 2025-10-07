"""tweak updated_at default and onupdate

Revision ID: b23c9e7d41af
Revises: cf2677145b90
Create Date: 2025-10-03 15:45:00.000000

"""

from datetime import datetime

import sqlalchemy as sa
from alembic import op

# revision identifiers, used by Alembic.
revision = "b23c9e7d41af"
down_revision = "cf2677145b90"
branch_labels = None
depends_on = None


def upgrade():
    # Убираем старый столбец updated_at (если был криво добавлен) и пересоздаём
    with op.batch_alter_table("decisions") as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            server_default=sa.text("CURRENT_TIMESTAMP"),
            existing_nullable=True,
        )

    # Для Postgres нужно явно прописать on update через триггер
    op.execute(
        """
    CREATE OR REPLACE FUNCTION update_updated_at_column()
    RETURNS TRIGGER AS $$
    BEGIN
        NEW.updated_at = now();
        RETURN NEW;
    END;
    $$ language 'plpgsql';
    """
    )

    op.execute(
        """
    DROP TRIGGER IF EXISTS set_updated_at ON decisions;
    CREATE TRIGGER set_updated_at
    BEFORE UPDATE ON decisions
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();
    """
    )


def downgrade():
    op.execute("DROP TRIGGER IF EXISTS set_updated_at ON decisions;")
    op.execute("DROP FUNCTION IF EXISTS update_updated_at_column;")
    with op.batch_alter_table("decisions") as batch_op:
        batch_op.alter_column(
            "updated_at",
            existing_type=sa.DateTime(),
            server_default=None,
            existing_nullable=True,
        )
