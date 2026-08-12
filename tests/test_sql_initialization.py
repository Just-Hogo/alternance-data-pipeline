import os
from pathlib import Path

import psycopg
import pytest

PROJECT_ROOT = Path(__file__).resolve().parents[1]
SQL_DIRECTORY = PROJECT_ROOT / "sql" / "initialization"

EXPECTED_TABLES = {
    "ingestion_runs",
    "job_offer_content",
    "job_offers",
}

EXPECTED_CUSTOM_INDEXES = {
    "idx_job_offer_content_diploma_level",
    "idx_job_offer_content_expiration",
    "idx_job_offer_content_rome_codes",
    "idx_job_offers_contract_start",
    "idx_job_offers_contract_types",
}


def execute_sql_initialization(connection: psycopg.Connection) -> None:
    with connection.cursor() as cursor:
        for path in sorted(SQL_DIRECTORY.glob("*.sql")):
            sql_content = path.read_text(encoding="utf-8")
            statements = [
                statement.strip()
                for statement in sql_content.split(";")
                if statement.strip()
            ]

            for statement in statements:
                cursor.execute(statement)


@pytest.fixture(scope="module")
def database_connection() -> psycopg.Connection:
    database_url = os.environ.get("TEST_DATABASE_URL")
    if database_url is None:
        pytest.skip("TEST_DATABASE_URL absent : test PostgreSQL non exécuté")

    with psycopg.connect(database_url, autocommit=True) as connection:
        yield connection


def test_sql_initialization_is_idempotent_and_creates_expected_objects(
    database_connection: psycopg.Connection,
) -> None:
    execute_sql_initialization(database_connection)
    execute_sql_initialization(database_connection)

    with database_connection.cursor() as cursor:
        cursor.execute(
            """
            SELECT table_name
            FROM information_schema.tables
            WHERE table_schema = 'lba'
            """
        )
        actual_tables = {row[0] for row in cursor.fetchall()}

        cursor.execute(
            """
            SELECT indexname
            FROM pg_indexes
            WHERE schemaname = 'lba'
              AND indexname LIKE 'idx_%'
            """
        )
        actual_custom_indexes = {row[0] for row in cursor.fetchall()}

    assert actual_tables == EXPECTED_TABLES
    assert actual_custom_indexes == EXPECTED_CUSTOM_INDEXES
