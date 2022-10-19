"""Контроллер для работы с БД SQLite."""
from sqlite3 import Connection, Cursor


class SQLiteController():
    """Класс контроллера для работы с БД SQLite."""

    conn: Connection
    curs: Cursor

    def __init__(self, connection: Connection) -> None:
        """Создаём курсор из полученного соединения.

        Parameters:
            connection: Соединение с SQLite.
        """
        self.conn = connection
        self.curs = connection.cursor()

    def extract(self, table_name: str) -> Cursor:
        """Извлечение данных из таблицы.

        Parameters:
            table_name: Имя таблицы.

        Returns:
            Курсор соединения для чтения полученных данных.
        """
        self.curs.execute(f'SELECT * FROM {table_name}')
        return self.curs
