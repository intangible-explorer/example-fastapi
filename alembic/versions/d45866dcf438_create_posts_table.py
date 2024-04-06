"""create posts table

Revision ID: d45866dcf438
Revises: 
Create Date: 2024-04-06 17:27:34.105501

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'd45866dcf438'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table("posts")

def downgrade() -> None:
    op.drop_table('posts')