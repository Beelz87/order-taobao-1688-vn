"""add address_in into shipment

Revision ID: b99c29024f1a
Revises: decaf7e9d344
Create Date: 2025-04-17 18:44:17.094715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b99c29024f1a'
down_revision = 'decaf7e9d344'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consignments', sa.Column('user_address_id', sa.Integer(), nullable=False))
    op.create_foreign_key(None, 'consignments', 'user_addresses', ['user_address_id'], ['id'])
    op.drop_column('consignments', 'shipping_address')
    op.drop_column('consignments', 'shipping_name')
    op.drop_column('consignments', 'shipping_phone_number')
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('consignments', sa.Column('shipping_phone_number', sa.VARCHAR(length=13), autoincrement=False, nullable=False))
    op.add_column('consignments', sa.Column('shipping_name', sa.VARCHAR(length=255), autoincrement=False, nullable=False))
    op.add_column('consignments', sa.Column('shipping_address', sa.VARCHAR(length=2056), autoincrement=False, nullable=False))
    op.drop_constraint(None, 'consignments', type_='foreignkey')
    op.drop_column('consignments', 'user_address_id')
    # ### end Alembic commands ###
