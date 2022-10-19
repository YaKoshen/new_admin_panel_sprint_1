"""Контроллер для работы с БД Postgres."""
from dataclasses import fields

from psycopg2.extensions import connection as postgres_connection
from psycopg2.extensions import cursor as postgres_cursor

from structures.common import sqlite_col
from structures.postgres import table_dataclass


class PostgresController():
    """Контроллер для работы с БД Postgres."""

    conn: postgres_connection
    curs: postgres_cursor

    def __init__(self, connection: postgres_connection) -> None:
        """Создаём курсор из полученного соединения.

        Parameters:
            connection: Соединение с Postgres.
        """
        self.conn = connection
        self.curs = connection.cursor()

    def insert(self, sqlite_chunk: tuple, table_name: str) -> None:
        """Запись данных в таблицу.

        Parameters:
            sqlite_chunk: Массив данных полученый из SQLite.
            table_name: Имя таблицы.
        """
        pg_dataclass_fields = tuple(field.name for field in fields(table_dataclass[table_name]))

        sqlite_columns = []
        pg_columns = []

        sqlite_keys = dict(sqlite_chunk[0]).keys()
        for pg_column in pg_dataclass_fields:
            sqlite_cloumn = sqlite_col(pg_column)
            if sqlite_cloumn in sqlite_keys:
                sqlite_columns.append(sqlite_cloumn)
                pg_columns.append(pg_column)

        data_template = '('+','.join('%s' for _ in pg_columns)+'), '
        query = f'INSERT INTO {table_name} ({", ".join(pg_columns)}) VALUES '

        data = []
        for sqlite_row in sqlite_chunk:
            query += data_template
            for sqlite_cloumn in sqlite_columns:
                data.append(dict(sqlite_row).get(sqlite_cloumn))
        query = query[:-2]
        query += ' ON CONFLICT(id) DO NOTHING'

        self.curs.execute(query, data)
        self.conn.commit()
