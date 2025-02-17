"""fix phone column

Revision ID: acf430ae2b28
Revises: 67bf146e776e
Create Date: 2025-02-17 11:20:26.354268

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'acf430ae2b28'
down_revision: Union[str, None] = '67bf146e776e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=13),
               nullable=False)
    op.create_unique_constraint(None, 'users', ['phone'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'users', type_='unique')
    op.alter_column('users', 'phone',
               existing_type=sa.VARCHAR(length=13),
               nullable=True)
    # ### end Alembic commands ###
