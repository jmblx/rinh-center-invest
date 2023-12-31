"""empty message

Revision ID: 2d4d7a22d8f8
Revises: 
Create Date: 2023-11-26 07:33:26.779914

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '2d4d7a22d8f8'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user',
    sa.Column('first_name', sa.String(), nullable=False),
    sa.Column('registered_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
    sa.Column('hashed_password', sa.String(length=1024), nullable=False),
    sa.Column('is_active', sa.Boolean(), nullable=False),
    sa.Column('is_superuser', sa.Boolean(), nullable=False),
    sa.Column('is_verified', sa.Boolean(), nullable=False),
    sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
    sa.Column('email', sa.String(length=320), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_table('request',
    sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('month', sa.Integer(), nullable=False),
    sa.Column('age', sa.Integer(), nullable=False),
    sa.Column('occupation', sa.String(), nullable=False),
    sa.Column('annual_income', sa.Integer(), nullable=False),
    sa.Column('monthly_inhand_salary', sa.Integer(), nullable=False),
    sa.Column('num_bank_accounts', sa.Integer(), nullable=False),
    sa.Column('num_credit_card', sa.Integer(), nullable=False),
    sa.Column('num_of_loan', sa.Integer(), nullable=False),
    sa.Column('num_credit_inquiries', sa.Integer(), nullable=False),
    sa.Column('credit_history_age', sa.Integer(), nullable=False),
    sa.Column('amount_invested_monthly', sa.Integer(), nullable=False),
    sa.Column('payment_behaviour', sa.String(), nullable=False),
    sa.Column('monthly_balance', sa.Integer(), nullable=False),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text("TIMEZONE('utc', now())"), nullable=True),
    sa.Column('is_good_client', sa.Float(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('request')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    # ### end Alembic commands ###
