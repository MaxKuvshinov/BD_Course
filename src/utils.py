import psycopg2


def create_db(database_name: str, **params: dict) -> None:
    """Создание базы данных"""

    conn = psycopg2.connect(dbname=database_name, **params)
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(f"DROP DATABASE {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        pass

    with conn.cursor() as cur:
        pass

    conn.commit()
    conn.close()


def save_db():
    pass
