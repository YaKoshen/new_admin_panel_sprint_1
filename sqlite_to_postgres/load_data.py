"""Скрипт для загрзки даннных их SQLite в Postgres."""
from sqlite3 import Connection as SQLiteConnection

from psycopg2.extensions import connection as postgres_coonnection
from tabulate import tabulate

from db_connections.postgres import postgres_conn_context
from db_connections.sqlite import sqlite_conn_context
from db_controllers.postgres import PostgresController
from db_controllers.sqlite import SQLiteController
from settings.settings import Settings
from structures.common import Timer, tables
from utils.logger import logger

timer = Timer()


def show_table_sizes(pg_connection: postgres_coonnection, sqlite_connection: SQLiteConnection) -> None:
    """Вывод в логи таблицы с размерами таблиц SQLite и Postgres.

    Parameters:
        pg_connection: Подключение к Postgres
        sqlite_connection: Подключение к SQLite
    """
    logger.info('Length of tables')
    length_data = []
    timer.start()
    for current_step, table in enumerate(tables):
        sqlite_curs.execute(f'SELECT COUNT(*) AS count FROM {table.sqlite}')
        table.sqlite_length = dict(sqlite_curs.fetchone()).get('count')

        pg_curs.execute(f'SELECT COUNT(*) FROM {table.postgres}')
        table.postgres_length = pg_curs.fetchone()[0]

        length_data.append((current_step+1, table.sqlite, table.postgres, table.sqlite_length, table.postgres_length,
                            table.sqlite_length == table.postgres_length))

    logger.info('\n'+tabulate(length_data, headers=('#', 'SQLite', 'Postgres', 'SQLite', 'Postgres', 'Equal')))
    logger.info(f'Length of tables got for {timer.get_value()}')


if __name__ == '__main__':
    # Работаем с подключениями к Postgres и SQLite через контестные менеджеры.
    with postgres_conn_context() as pg_conn, sqlite_conn_context() as sqlite_conn:
        logger.info('Start to copy data from SQLite to Postgres\n')

        pg_curs = pg_conn.cursor()
        sqlite_curs = sqlite_conn.cursor()

        show_table_sizes(pg_conn, sqlite_conn)

        ans = input('Do you whant to delete data from Postgres tables? [Y/n] ')
        if ans.strip().lower() == 'y':
            for table in tables:
                ans = input(f'Do you whant to delete data from {table.postgres}? [Y/n] ')
                if ans.strip().lower() == 'y':
                    timer.start()
                    pg_curs.execute(f'TRUNCATE TABLE {table.postgres} CASCADE')
                    pg_conn.commit()
                    logger.info(f'{table.postgres} erased for {timer.get_value()}')
        else:
            logger.info('Skip erasing data')
        logger.info('')

        logger.info(f'Copy data from SQLite to Postgres with chunk size = {Settings().chunk_size}')
        timer.start()

        pg_ctrl = PostgresController(pg_conn)
        sqlite_ctrl = SQLiteController(sqlite_conn)

        tables_count = len(tables)
        for current_step, table in enumerate(tables):
            logger.info(f'Step {current_step + 1}/{tables_count}.')
            logger.info(f'Copy from {table.sqlite}(SQLite) to {table.postgres}(Postgres)')

            sqlite_curs = sqlite_ctrl.extract(table.sqlite)
            copied_rows = 0
            while sqlite_chunk := sqlite_curs.fetchmany(Settings().chunk_size):
                pg_ctrl.insert(sqlite_chunk, table.postgres)
                copied_rows += len(sqlite_chunk)
                logger.info(f'Copied {copied_rows}/{table.sqlite_length} rows')

        logger.info(f'Copied all data from SQLite to Postgres for {timer.get_value()}')

    logger.info('All works done')
