import datetime
from dataclasses import dataclass, field


@dataclass
class TablePair:
    postgres: str
    sqlite: str
    postgres_columns: tuple
    postgres_length: int = field(default=None)
    sqlite_length: int = field(default=None)


tables = (
    TablePair(sqlite='film_work', postgres='content.filmwork',
        postgres_columns=('created', 'modified', 'id', 'title', 'description', 'creation_date', 'rating', 'type',
                          'file_path')),
    TablePair(sqlite='genre', postgres='content.genre',
        postgres_columns = ('created', 'modified', 'id', 'name', 'description')),
    TablePair(sqlite='genre_film_work', postgres='content.genre_filmwork',
        postgres_columns = ('id', 'created', 'filmwork_id', 'genre_id')),
    TablePair(sqlite='person', postgres='content.person',
        postgres_columns = ('created', 'modified', 'id', 'full_name', 'gender')),
    TablePair(sqlite='person_film_work', postgres='content.person_filmwork',
        postgres_columns = ('id', 'role', 'created', 'filmwork_id', 'person_id')),
)


postgres_sqlite_columns = {
    'created': 'created_at',
    'modified': 'updated_at',
    'filmwork_id': 'film_work_id',
}


def sqlite_col(postgres_column_name: str) -> str:
    if postgres_column_name in postgres_sqlite_columns:
        return postgres_sqlite_columns[postgres_column_name]

    return postgres_column_name


sqlite_postgres_columns = {
    'created_at': 'created',
    'updated_at': 'modified',
    'film_work_id': 'filmwork_id',
}


def postgres_col(sqlite_column_name: str) -> str:
    if sqlite_column_name in sqlite_postgres_columns:
        return sqlite_postgres_columns[sqlite_column_name]

    return sqlite_column_name


class Timer:
    start_time = None

    def start(self):
        self.start_time = datetime.datetime.now()

    def get_value(self):
        return datetime.datetime.now() - self.start_time

    def __init__(self):
        self.start()
