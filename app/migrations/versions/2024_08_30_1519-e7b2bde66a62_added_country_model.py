"""added country model

Revision ID: e7b2bde66a62
Revises: c8d3a921e0da
Create Date: 2024-08-30 15:19:51.205807

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e7b2bde66a62'
down_revision = 'c8d3a921e0da'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('countries',
    sa.Column('name', sa.String(length=45), nullable=False),
    sa.Column('created_by', sa.String(length=50), nullable=False),
    sa.Column('id', sa.Integer(), autoincrement=True, nullable=False),
    sa.Column('uuid', sa.String(length=50), nullable=False),
    sa.Column('date', sa.Date(), server_default=sa.text('CURRENT_DATE'), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.Column('last_modified', sa.DateTime(), server_default=sa.text('now()'), nullable=False),
    sa.ForeignKeyConstraint(['created_by'], ['users.uuid'], ),
    sa.PrimaryKeyConstraint('id'),
    sa.UniqueConstraint('name'),
    sa.UniqueConstraint('uuid')
    )
    op.create_index(op.f('ix_countries_created_at'), 'countries', ['created_at'], unique=False)
    op.create_index(op.f('ix_countries_date'), 'countries', ['date'], unique=False)
    op.add_column('states', sa.Column('country_id', sa.String(length=45), nullable=False))
    op.create_foreign_key(None, 'states', 'countries', ['country_id'], ['uuid'])
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_constraint(None, 'states', type_='foreignkey')
    op.drop_column('states', 'country_id')
    op.drop_index(op.f('ix_countries_date'), table_name='countries')
    op.drop_index(op.f('ix_countries_created_at'), table_name='countries')
    op.drop_table('countries')
    # ### end Alembic commands ###