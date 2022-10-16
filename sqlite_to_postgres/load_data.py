from db_connections.postgres import postgres_conn_context
from db_connections.sqlite import sqlite_conn_context


if __name__ == '__main__':
    with postgres_conn_context() as pg_conn, sqlite_conn_context() as sqlite_conn:
        query = 'SELECT * FROM content.filmwork LIMIT 10'

        pg_curs = pg_conn.cursor()
        pg_curs.execute(query)

        print(pg_curs.fetchall())
