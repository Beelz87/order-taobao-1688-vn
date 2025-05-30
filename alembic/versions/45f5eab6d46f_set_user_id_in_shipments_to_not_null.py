"""Set user_id in shipments to NOT NULL

Revision ID: 45f5eab6d46f
Revises: b5420e5b19db
Create Date: 2025-05-21 23:35:45.970962

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '45f5eab6d46f'
down_revision = 'b5420e5b19db'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('fulfillments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    op.alter_column('shipments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=False)
    # op.create_unique_constraint('unique_user_role', 'user_roles', ['user_id', 'role_id'])
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint('unique_user_role', 'user_roles', type_='unique')
    op.alter_column('shipments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    op.alter_column('fulfillments', 'user_id',
               existing_type=sa.INTEGER(),
               nullable=True)
    # ### end Alembic commands ###
