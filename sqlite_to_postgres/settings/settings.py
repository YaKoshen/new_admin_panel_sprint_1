from pydantic import BaseSettings


class Settings(BaseSettings):
    pg_dbname: str
    pg_user: str
    pg_password: str
    pg_host: str
    pg_port: int = 5432

    sqlite_db_path: str

    chunk_size: int

    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'
