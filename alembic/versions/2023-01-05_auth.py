"""auth

Revision ID: d40f40264827
Revises:
Create Date: 2023-01-05 12:08:49.446747

"""
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from alembic import op

# revision identifiers, used by Alembic.
revision = "d40f40264827"
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "auth_user",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("email", sa.String(), nullable=False),
        sa.Column("password", sa.LargeBinary(), nullable=False),
        sa.Column("is_admin", sa.Boolean(), server_default="false", nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.PrimaryKeyConstraint("id", name=op.f("auth_user_pkey")),
    )
    op.create_table(
        "auth_refresh_token",
        sa.Column("uuid", postgresql.UUID(), nullable=False),
        sa.Column("user_id", sa.Integer(), nullable=False),
        sa.Column("refresh_token", sa.String(), nullable=False),
        sa.Column("expires_at", sa.DateTime(), nullable=False),
        sa.Column(
            "created_at", sa.DateTime(), server_default=sa.text("now()"), nullable=False
        ),
        sa.Column("updated_at", sa.DateTime(), nullable=True),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth_user.id"],
            name=op.f("auth_refresh_token_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.PrimaryKeyConstraint("uuid", name=op.f("auth_refresh_token_pkey")),
    )


def downgrade() -> None:
    op.drop_table("auth_refresh_token")
    op.drop_table("auth_user")
