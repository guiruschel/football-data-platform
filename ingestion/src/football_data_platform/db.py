"""Create the raw schema and load annotated match rows into PostgreSQL."""

from __future__ import annotations

import psycopg2
from psycopg2.extras import Json, execute_values
import pandas as pd

from .config import LoaderConfig


DDL = """
CREATE SCHEMA IF NOT EXISTS football_source;

CREATE TABLE IF NOT EXISTS football_source.raw_matches (
    id BIGSERIAL PRIMARY KEY,
    competition_name TEXT NOT NULL,
    competition_code TEXT NOT NULL,
    season_label TEXT NOT NULL,
    season_code TEXT NOT NULL,
    source_url TEXT NOT NULL,
    source_row_number INTEGER NOT NULL,
    payload JSONB NOT NULL,
    ingested_at TIMESTAMPTZ NOT NULL DEFAULT NOW(),
    UNIQUE (competition_code, season_code, source_row_number)
);
"""


# Open a connection to the SOURCE PostgreSQL database.
def connect_to_source(config: LoaderConfig):
    return psycopg2.connect(
        host=config.source_host,
        port=config.source_port,
        dbname=config.source_db,
        user=config.source_user,
        password=config.source_password,
    )


# Create the schema and table used for raw ingestion.
def ensure_schema_and_table(connection) -> None:
    with connection.cursor() as cursor:
        cursor.execute(DDL)
    connection.commit()


# Convert a DataFrame row to a JSON-safe dictionary.
def row_to_payload(row: pd.Series) -> dict:
    return {key: (None if pd.isna(value) else value) for key, value in row.to_dict().items()}


# Insert a DataFrame into the raw ingestion table with idempotent upserts.
def load_frame(
    connection,
    frame: pd.DataFrame,
    competition_name: str,
    competition_code: str,
    season_label: str,
    season_code: str,
    source_url: str,
) -> int:
    records = [
        (
            competition_name,
            competition_code,
            season_label,
            season_code,
            source_url,
            index,
            Json(row_to_payload(row)),
        )
        for index, (_, row) in enumerate(frame.iterrows(), start=1)
    ]

    if not records:
        return 0

    statement = """
        INSERT INTO football_source.raw_matches (
            competition_name,
            competition_code,
            season_label,
            season_code,
            source_url,
            source_row_number,
            payload
        ) VALUES %s
        ON CONFLICT (competition_code, season_code, source_row_number)
        DO UPDATE SET
            competition_name = EXCLUDED.competition_name,
            source_url = EXCLUDED.source_url,
            payload = EXCLUDED.payload,
            ingested_at = NOW();
    """

    with connection.cursor() as cursor:
        execute_values(cursor, statement, records, template="(%s, %s, %s, %s, %s, %s, %s)")

    connection.commit()
    return len(records)
