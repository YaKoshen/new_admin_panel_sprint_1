import pytest

from db_connections.postgres import postgres_conn_context
from db_connections.sqlite import sqlite_conn_context
from structures.common import tables

def test_rows_count():
    """Количество строк в таблицах совпадают."""
    with postgres_conn_context() as pg_conn, sqlite_conn_context() as sqlite_conn:
        pg_curs = pg_conn.cursor()
        sqlite_curs = sqlite_conn.cursor()
        for table in tables:
            sqlite_curs.execute(f'SELECT COUNT(*) AS count FROM {table.sqlite}')
            sqlite_length = int(dict(sqlite_curs.fetchone()).get('count'))

            pg_curs.execute(f'SELECT COUNT(*) FROM {table.postgres}')
            postgres_length = int(pg_curs.fetchone()[0])

            assert sqlite_length == postgres_length

def test_rows_values():
    """Проверка значений."""
    with postgres_conn_context() as pg_conn, sqlite_conn_context() as sqlite_conn:
        pg_curs = pg_conn.cursor()
        sqlite_curs = sqlite_conn.cursor()
        # TODO Добавить сравнение строк в таблицах
