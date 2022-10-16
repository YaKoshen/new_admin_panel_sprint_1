"""Скрипт для загрзки даннных их SQLite в Postgres."""
from tabulate import tabulate

from db_connections.postgres import postgres_conn_context
from db_connections.sqlite import sqlite_conn_context
from settings.settings import Settings
from structures.common import TablePair, Timer, sqlite_col, tables


def generate_pg_insert_query(table: TablePair, sqlite_rows: list()) -> tuple():
    """Генерипует запрос и даные для записи в Postgres.

    Args:
        table: Имя таблицы.
        sqlite_rows: Массив строк из SQLite.

    Returns:
        Строку запроса в Postgres для вставки и список значений для колонок из SQLite.

    """
    sqlite_columns = []
    postgres_columns = []

    sqlite_keys = dict(sqlite_rows[0]).keys()
    for postgres_column in table.postgres_columns:
        sqlite_cloumn = sqlite_col(postgres_column)
        if sqlite_cloumn in sqlite_keys:
            sqlite_columns.append(sqlite_cloumn)
            postgres_columns.append(postgres_column)

    data_template = '('+','.join('%s' for _ in postgres_columns)+'), '
    query = f'INSERT INTO {table.postgres} ({", ".join(postgres_columns)}) VALUES '

    data = []
    for sqlite_row in sqlite_rows:
        query += data_template
        for sqlite_cloumn in sqlite_columns:
            data.append(dict(sqlite_row).get(sqlite_cloumn))
    query = query[:-2]
    query += ' ON CONFLICT(id) DO NOTHING'

    return (query, data)

if __name__ == '__main__':
    """Работаем с подключениями к Postgres и SQLite через контестные менеджеры."""
    with postgres_conn_context() as pg_conn, sqlite_conn_context() as sqlite_conn:
        print(f'Start to copy data drom SQLite to Postgres\n')

        pg_curs = pg_conn.cursor()
        sqlite_curs = sqlite_conn.cursor()

        print('Length of tables')
        timer = Timer()
        length_data = []
        for current_step, table in enumerate(tables):
            sqlite_curs.execute(f'SELECT COUNT(*) AS count FROM {table.sqlite}')
            table.sqlite_length = dict(sqlite_curs.fetchone()).get('count')

            pg_curs.execute(f'SELECT COUNT(*) FROM {table.postgres}')
            table.postgres_length = pg_curs.fetchone()[0]

            length_data.append((current_step+1, table.sqlite, table.postgres, table.sqlite_length,
                table.postgres_length, table.sqlite_length == table.postgres_length))

        print(tabulate(length_data, headers=('#', 'SQLite', 'Postgres', 'SQLite', 'Postgres', 'Equal')))
        print(f'\nLength of tables got for {timer.get_value()}')

        ans = input('Do you whant to delete data from Postgres tables? (Y/n) ')
        if ans.strip().lower() == 'y':
            for table in tables:
                ans = input(f'Do you whant to delete data from {table.postgres}? (Y/n) ')
                if ans.strip().lower() == 'y':
                    timer.start()
                    pg_curs.execute(f'TRUNCATE TABLE {table.postgres} CASCADE')
                    pg_conn.commit()
                    print(f'{table.postgres} erased for {timer.get_value()}')
        else:
            print('Skip erasing data')
        print('')

        print(f'Copy data from SQLite to Postgres with chunk size = {Settings().chunk_size}')
        timer.start()
        for current_step, table in enumerate(tables):
            print(f'Copy data from {table.sqlite} (SQLite) to {table.postgres} (Postgres)')
            sqlite_curs.execute(f'SELECT * FROM {table.sqlite}')
            copied_rows = 0
            while True:
                sqlite_chunk = sqlite_curs.fetchmany(Settings().chunk_size)
                if not sqlite_chunk:
                    break

                query, data = generate_pg_insert_query(table, sqlite_chunk)
                pg_curs.execute(query, data)
                pg_conn.commit()

                copied_rows += len(sqlite_chunk)
                print(f'Copied {copied_rows}/{table.sqlite_length} rows')

        print(f'Copied all data from SQLite to Postgres for {timer.get_value()}')

    print('All works done')
