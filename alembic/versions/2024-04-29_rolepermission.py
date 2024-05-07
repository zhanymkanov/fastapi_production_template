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
        "role_permissions",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("permissions", sa.JSON(), sa.Identity(always=False), nullable=False),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            ondelete="CASCADE",
        )
        
    )
    op.create_table(
        "user_roles",
        sa.Column("id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("user_id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.Column("role_id", sa.Integer(), sa.Identity(always=False), nullable=False),
        sa.ForeignKeyConstraint(
            ["user_id"],
            ["auth_user.id"],
            name=op.f("auth_refresh_token_user_id_fkey"),
            ondelete="CASCADE",
        ),
        sa.ForeignKeyConstraint(
            ["role_id"],
            ["roles.id"],
            ondelete="CASCADE",
        )
        
    )


def downgrade() -> None:
    op.drop_table("roles")
    op.drop_table("permissions")
    op.drop_table("role_permissions")
    op.drop_table("user_roles")
