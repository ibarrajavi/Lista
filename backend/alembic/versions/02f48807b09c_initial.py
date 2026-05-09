"""initial

Revision ID: 02f48807b09c
Revises:
Create Date: 2026-03-28 12:22:24.962678

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
import sqlalchemy.dialects.postgresql as pg


# revision identifiers, used by Alembic.
revision: str = '02f48807b09c'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        'users',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('first_name', sa.String(150), nullable=False),
        sa.Column('last_name', sa.String(150), nullable=False),
        sa.Column('username', sa.String(150), nullable=False),
        sa.Column('hashed_pw', sa.String(256), nullable=False),
        sa.Column('refresh_hash', sa.String(256), nullable=True),
        sa.Column('email', sa.String(254), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.Column('verified_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_users_username'), 'users', ['username'], unique=True)
    op.create_index(op.f('ix_users_email'), 'users', ['email'], unique=True)

    op.create_table(
        'list',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('name', sa.String(150), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_list_name'), 'list', ['name'], unique=False)
    op.create_index(op.f('ix_list_user_id'), 'list', ['user_id'], unique=False)

    op.create_table(
        'task',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('list_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('description', sa.String(256), nullable=False),
        sa.Column('position', sa.Integer(), nullable=False),
        sa.Column('is_complete', sa.Boolean(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('updated_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['list_id'], ['list.id']),
        sa.PrimaryKeyConstraint('id'),
    )
    op.create_index(op.f('ix_task_list_id'), 'task', ['list_id'], unique=False)

    op.create_table(
        'verification_tokens',
        sa.Column('id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('user_id', pg.UUID(as_uuid=True), nullable=False),
        sa.Column('token_hash', sa.String(256), nullable=False),
        sa.Column('type', sa.String(50), nullable=False),
        sa.Column('expires_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.ForeignKeyConstraint(['user_id'], ['users.id']),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('token_hash'),
    )
    op.create_index(op.f('ix_verification_tokens_user_id'), 'verification_tokens', ['user_id'], unique=False)


def downgrade() -> None:
    op.drop_index(op.f('ix_verification_tokens_user_id'), table_name='verification_tokens')
    op.drop_table('verification_tokens')
    op.drop_index(op.f('ix_task_list_id'), table_name='task')
    op.drop_table('task')
    op.drop_index(op.f('ix_list_user_id'), table_name='list')
    op.drop_index(op.f('ix_list_name'), table_name='list')
    op.drop_table('list')
    op.drop_index(op.f('ix_users_email'), table_name='users')
    op.drop_index(op.f('ix_users_username'), table_name='users')
    op.drop_table('users')
