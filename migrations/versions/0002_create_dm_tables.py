"""

Revision ID: 0002_create_dm_tables
Revises: 0001_create_dm_datetime
Create Date: 2018-02-09 12:01:49.592019

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

revision = '0002_create_dm_tables'
down_revision = '0001_create_dm_datetime'


def upgrade():

    # Create dm_organisation table
    op.create_table('dm_organisation',
                    sa.Column('organisation_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('organisation_name', sa.String(), nullable=True),
                    sa.PrimaryKeyConstraint('organisation_id')
                    )

    # Create dm_service table - recreate all the columns in operation DB
    op.create_table('dm_service',
                    sa.Column('service_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('service_name', sa.String(), nullable=True),
                    sa.Column('organisation', sa.Text(), nullable=True),
                    sa.Column('crown', sa.Text(), nullable=True),
                    sa.Column('research_mode', sa.Boolean(), nullable=True),
                    sa.Column('restricted', sa.Text(), nullable=True),
                    sa.Column('active', sa.Text(), nullable=True),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    sa.Column('email_from', sa.String(), nullable=True),
                    sa.Column('organisation_type', sa.Text, nullable=True),
                    sa.PrimaryKeyConstraint('service_id')
                    )

    # Create dm_template table
    op.create_table('dm_template',
                    sa.Column('template_id', postgresql.UUID(as_uuid=True), nullable=False),
                    sa.Column('template_name', sa.String(), nullable=True),
                    sa.Column('type', sa.Enum('email', 'sms', 'letter', name='template_type'), nullable=True),
                    sa.Column('service_id', postgresql.UUID(as_uuid=True), nullable=True),
                    sa.PrimaryKeyConstraint('template_id'),
                    sa.Column('created_at', sa.DateTime(), nullable=True),
                    sa.Column('updated_at', sa.DateTime(), nullable=True),
                    #sa.ForeignKeyConstraint(['service_id'], ['dm_service.service_id'], ondelete="CASCADE"),
                    )

def downgrade():
    op.execute("drop type if exists template_types cascade")
    op.drop_table('dm_template')  # drop template first because it has a foreign key on dm_service
    op.drop_table('dm_service')
    op.drop_table('dm_organisation')
