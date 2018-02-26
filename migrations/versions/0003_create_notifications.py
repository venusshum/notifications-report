"""

Revision ID: 142296f579c9
Revises: 0002_create_dm_tables
Create Date: 2018-02-19 19:05:48.216726

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0003_create_notifications'
down_revision = '0002_create_dm_tables'


def upgrade():
    # Create notifications_for_today table
    op.create_table('notifications_for_today',
                    sa.Column('notification_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('dm_template', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('dm_datetime', sa.Date(), nullable=True),
                    sa.Column('dm_service', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('notification_type', sa.Enum('email', 'sms', 'letter', name='notification_type'), nullable=True),
                    sa.Column('provider', sa.Text(), nullable=True),
                    sa.Column('rate_multiplier', sa.Numeric(), nullable=True),
                    sa.Column('international', sa.Boolean(), nullable=True),
                    sa.Column('provider_rate', sa.Numeric(), nullable=True),
                    sa.Column('client_rate', sa.Numeric(), nullable=True),
                    sa.Column('billable_unit', sa.Numeric(), nullable=True),
                    sa.Column('notifications_sent', sa.Integer(), nullable=True),
                    sa.PrimaryKeyConstraint('dm_template', 'dm_datetime', 'rate_multiplier')
                    )

    # Create notifications_for_today table
    op.create_table('ft_billing',
                    sa.Column('dm_template', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('dm_datetime', sa.Date(), nullable=True),
                    sa.Column('dm_service', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.Column('notification_type', sa.Text(), nullable=True),
                    sa.Column('provider', sa.Text(), nullable=True),
                    sa.Column('rate_multiplier', sa.Numeric(), nullable=True),
                    sa.Column('international', sa.Boolean(), nullable=True),
                    sa.Column('provider_rate', sa.Numeric(), nullable=True),
                    sa.Column('client_rate', sa.Numeric(), nullable=True),
                    sa.Column('billable_unit', sa.Numeric(), nullable=True),
                    sa.Column('notifications_sent', sa.Integer(), nullable=True),
                    sa.Column('billing_total', sa.Numeric(), nullable=True),
                    sa.PrimaryKeyConstraint('dm_template', 'dm_datetime', 'rate_multiplier')
                    )


def downgrade():
    op.drop_table('notifications_for_today')
    op.drop_table('ft_billing')