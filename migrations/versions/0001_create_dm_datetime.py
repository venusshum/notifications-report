"""

Revision ID: 0001_create_dm_datetime
Revises: None
Create Date: 2018-02-09 11:21:50.596117

"""
from alembic import op
import sqlalchemy as sa

revision = '0001_create_dm_datetime'
down_revision = None


def upgrade():
    # Create dm_datetime table
    op.create_table('dm_datetime',
                    sa.Column('bst_date', sa.Date(), nullable=False),
                    sa.Column('year', sa.Integer(), nullable=False),
                    sa.Column('month', sa.Integer(), nullable=False),
                    sa.Column('month_name', sa.String(), nullable=False),
                    sa.Column('day', sa.Integer(), nullable=True),
                    sa.Column('bst_day', sa.Integer(), nullable=False),
                    sa.Column('day_of_year', sa.Integer(), nullable=False),
                    sa.Column('week_day_name', sa.String(), nullable=False),
                    sa.Column('calendar_week', sa.Integer(), nullable=True),
                    sa.Column('quartal', sa.String(), nullable=False),
                    sa.Column('year_quartal', sa.String(), nullable=False),
                    sa.Column('year_month', sa.String(), nullable=False),
                    sa.Column('year_calendar_week', sa.String(), nullable=False),
                    sa.Column('financial_year', sa.Integer(), nullable=True),
                    sa.Column('utc_daytime_start', sa.DateTime(), nullable=False),
                    sa.Column('utc_daytime_end', sa.DateTime(), nullable=False),
                    sa.PrimaryKeyConstraint('bst_date')
                    )
    # Set indexes
    op.create_index(op.f('ix_dm_datetime_yearmonth'), 'dm_datetime', ['year', 'month'], unique=False)

    # Insert data into table
    op.execute(
        """
        INSERT into dm_datetime (
        SELECT
        datum AS bst_date,
        EXTRACT(YEAR FROM datum) AS year,
        EXTRACT(MONTH FROM datum) AS month,
        -- Localized month name
        to_char(datum, 'TMMonth') AS month_name,
        EXTRACT(DAY FROM datum) AS day,
        EXTRACT(DAY FROM datum) AS bst_day,
        EXTRACT(DOY FROM datum) AS day_of_year,
        -- Localized weekday
        to_char(datum, 'TMDay') AS week_day_name,
        -- ISO calendar week
        EXTRACT(week FROM datum) AS calendar_week,
        'Q' || to_char(datum, 'Q') AS quartal,
        to_char(datum, 'yyyy/"Q"Q') AS year_quartal,
        to_char(datum, 'yyyy/mm') AS year_month,
        -- ISO calendar year and week
        to_char(datum, 'iyyy/IW') AS year_calendar_week,
        (SELECT CASE WHEN (extract(month from datum) <= 3) THEN (extract(year FROM datum) -1)
        ELSE (extract(year FROM datum)) end),
        (datum + TIME '00:00:00') at TIME zone 'utc' as utc_daytime_start,	-- convert bst time to utc time
        (datum + TIME '23:59:59') at TIME zone 'utc' as utc_daytime_end
        FROM (
        -- There are 5 leap years in this range, so calculate 365 * 20 + 5 records
        SELECT '2015-01-01'::date + SEQUENCE.DAY AS datum
        FROM generate_series(0,365*20+5) AS SEQUENCE(DAY)
        GROUP BY SEQUENCE.day
        ) DQ
        ORDER BY bst_date
        );
        """
    )


def downgrade():
    op.drop_table('dm_datetime')
