# Скрипты для работы с Postgesql

Содержимое этой папки не входит в проектное задание.
Файлы используются для работы в ОС Windows с использованием WSL.

Состав файлов:
- `docker_postgres_create.bat` создаёт докер контейнер с Postgresql (Windows)
- `docker_postgres_run.bat` запускает созданный докер контейнер с Postgresql (Windows)
- `fill_table.py` заполненяет таблицы `content.person` и `content.person_film_work`
- `film_work_data.sql` заполняет таблицу `content.film_work`
- `postgres_psql.sh` запуск команды `psql` с необходимыми парраметрами (Linux)
