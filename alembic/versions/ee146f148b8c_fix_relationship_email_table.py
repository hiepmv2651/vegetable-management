"""fix relationship Email table

Revision ID: ee146f148b8c
Revises: 7aa3477f19ac
Create Date: 2024-01-17 09:37:07.912184

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ee146f148b8c'
down_revision: Union[str, None] = '7aa3477f19ac'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('emails_ibfk_2', 'emails', type_='foreignkey')
    op.create_foreign_key(None, 'emails', 'employees', ['sender_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'emails', type_='foreignkey')
    op.create_foreign_key('emails_ibfk_2', 'emails', 'users', ['sender_id'], ['id'], ondelete='CASCADE')
    # ### end Alembic commands ###