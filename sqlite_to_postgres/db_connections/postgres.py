from contextlib import contextmanager

import psycopg2
from psycopg2.extras import DictCursor

from settings.settings import Settings

CONNECTION_CONFIG = {
    'dbname': Settings().pg_dbname,
    'user': Settings().pg_user,
    'password': Settings().pg_password,
    'host': Settings().pg_host,
    'port': Settings().pg_port
}

@contextmanager
def postgres_conn_context():
    conn = psycopg2.connect(**CONNECTION_CONFIG, cursor_factory=DictCursor)
    yield conn

    conn.close()
