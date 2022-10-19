"""Класс с контекстом для подключения к SQLite."""
import sqlite3
from contextlib import contextmanager

from settings.settings import Settings


@contextmanager
def sqlite_conn_context():
    """Контекст-именеджер для подключения к SQLite.

    Yields:
        conn: Соединение с SQLite.
    """
    conn = sqlite3.connect(Settings().sqlite_db_path)
    conn.row_factory = sqlite3.Row
    yield conn

    conn.close()
