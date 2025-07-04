"""document_summary table added

Revision ID: 720e1647ed9b
Revises: 92acc645abec
Create Date: 2025-06-28 23:53:09.007418

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision: str = '720e1647ed9b'
down_revision: Union[str, None] = '92acc645abec'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_cmetadata_gin'), table_name='langchain_pg_embedding', postgresql_using='gin')
    op.drop_table('langchain_pg_embedding')
    op.drop_table('langchain_pg_collection')
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('langchain_pg_collection',
    sa.Column('uuid', sa.UUID(), autoincrement=False, nullable=False),
    sa.Column('name', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('cmetadata', postgresql.JSON(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.PrimaryKeyConstraint('uuid', name='langchain_pg_collection_pkey'),
    sa.UniqueConstraint('name', name='langchain_pg_collection_name_key', postgresql_include=[], postgresql_nulls_not_distinct=False),
    postgresql_ignore_search_path=False
    )
    op.create_table('langchain_pg_embedding',
    sa.Column('id', sa.VARCHAR(), autoincrement=False, nullable=False),
    sa.Column('collection_id', sa.UUID(), autoincrement=False, nullable=True),
    sa.Column('embedding', sa.NullType(), autoincrement=False, nullable=True),
    sa.Column('document', sa.VARCHAR(), autoincrement=False, nullable=True),
    sa.Column('cmetadata', postgresql.JSONB(astext_type=sa.Text()), autoincrement=False, nullable=True),
    sa.ForeignKeyConstraint(['collection_id'], ['langchain_pg_collection.uuid'], name=op.f('langchain_pg_embedding_collection_id_fkey'), ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('id', name=op.f('langchain_pg_embedding_pkey'))
    )
    op.create_index(op.f('ix_cmetadata_gin'), 'langchain_pg_embedding', ['cmetadata'], unique=False, postgresql_using='gin')
    # ### end Alembic commands ###
