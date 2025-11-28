"""initial schema

Revision ID: 0001_init
Revises: 
Create Date: 2025-11-25 13:37:00

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '0001_init'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        'query_logs',
        sa.Column('id', sa.Integer(), primary_key=True, nullable=False),
        sa.Column('question', sa.Text(), nullable=False),
        sa.Column('answer', sa.Text(), nullable=False),
        sa.Column('sources', sa.String(), nullable=True),
        sa.Column('input_tokens', sa.Integer(), nullable=True),
        sa.Column('output_tokens', sa.Integer(), nullable=True),
        sa.Column('response_time_ms', sa.Integer(), nullable=True),
        sa.Column('created_at', sa.DateTime(), server_default=sa.text('CURRENT_TIMESTAMP'), nullable=True),
    )
    # Индексы, соответствующие актуальной модели QueryLog
    op.create_index('ix_query_logs_response_time_ms', 'query_logs', ['response_time_ms'])
    # Составной индекс для пагинации «медленных» записей. 
    op.create_index('ix_query_logs_slowest', 'query_logs', ['response_time_ms', 'id'])
    # Индекс по дате создания — для выборок последних логов и очисток по времени
    op.create_index('ix_query_logs_created_at', 'query_logs', ['created_at'])


def downgrade() -> None:
    op.drop_index('ix_query_logs_created_at', table_name='query_logs')
    op.drop_index('ix_query_logs_slowest', table_name='query_logs')
    op.drop_index('ix_query_logs_response_time_ms', table_name='query_logs')
    op.drop_table('query_logs')
