"""create courses, professors, users, and prof_course junction table

Revision ID: 009e34c9391a
Revises: 
Create Date: 2022-11-02 23:13:07.276005

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '009e34c9391a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'courses', 
        sa.Column('id', sa.Integer(), nullable=False, primary_key=True),
        sa.Column('name'),
        sa.Column('created_at')
    )


def downgrade() -> None:
    pass
