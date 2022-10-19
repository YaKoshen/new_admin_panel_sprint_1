"""Класс с контекстом для подключения к Postgres."""
from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from settings.settings import Settings


@contextmanager
def postgres_conn_context():
    """Контекст-именеджер для подключения к Postgres.

    Yields:
        conn: Соединение с Postgres.
    """
    connection_config = {
        'dbname': Settings().pg_dbname,
        'user': Settings().pg_user,
        'password': Settings().pg_password,
        'host': Settings().pg_host,
        'port': Settings().pg_port,
    }

    conn = psycopg2.connect(**connection_config, cursor_factory=DictCursor)
    yield conn

    conn.close()
