import psycopg2


def create_db(database_name: str, **params: dict) -> None:
    """Создание базы данных"""

    conn = psycopg2.connect(dbname='postgres', **params)
    conn.autocommit = True

    cur = conn.cursor()

    cur.execute(f"DROP DATABASE IF EXISTS {database_name}")
    cur.execute(f"CREATE DATABASE {database_name}")

    conn.close()

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS companies (
                company_id SERIAL PRIMARY KEY,
                company_name VARCHAR(255) NOT NULL,
                company_url VARCHAR(255)
            )
        """)

    with conn.cursor() as cur:
        cur.execute("""
            CREATE TABLE IF NOT EXISTS vacancies (
                company_id INTEGER NOT NULL REFERENCES companies(company_id),
                vacancy_name VARCHAR(255) NOT NULL,
                vacancy_url VARCHAR(255),
                salary_from NUMERIC,
                salary_to NUMERIC,
                currency VARCHAR(10),
                description TEXT,
                experience VARCHAR(255),
                requirement TEXT
            )
        """)

    conn.commit()
    conn.close()


def insert_data(data, database_name, **params):
    """Вставка данных о компаниях и вакансиях в БД"""

    conn = psycopg2.connect(dbname=database_name, **params)

    with conn.cursor() as cur:
        for item in data:
            # Вставляем данные о компании в таблицу companies
            cur.execute("""
                INSERT INTO companies (company_id, company_name, company_url)
                VALUES (%s, %s, %s)
                ON CONFLICT (company_id) DO NOTHING
            """, (item['company_id'], item['company_name'], item['company_url']))

            # Вставляем данные о вакансии в таблицу vacancies
            cur.execute("""
                INSERT INTO vacancies (
                    company_id, vacancy_name, vacancy_url, salary_from,
                    salary_to, currency, description, experience, requirement
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (
                item['company_id'], item['vacancy_name'], item['vacancy_url'],
                item['salary_from'], item['salary_to'], item['currency'],
                item['description'], item['experience'], item['requirement']
            ))

    conn.commit()
    conn.close()
