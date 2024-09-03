import psycopg2
from typing import List, Optional, Tuple, Any


class DBManager:
    """Класс, для подключения к БД PostgreSQL"""

    def __init__(self, database_name, **params):
        self.database_name = database_name
        self.params = params
        self.conn = psycopg2.connect(dbname=database_name, **params)

    def __del__(self) -> None:
        self.conn.close()

    def get_companies_and_vacancies_count(self):
        """Получает список всех компаний и количество вакансий у каждой компании."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.company_name, COUNT(vacancies.vacancy_url)
                FROM companies
                LEFT JOIN vacancies ON companies.company_id = vacancies.company_id
                GROUP BY companies.company_name
            """
            )
            return cur.fetchall()

    def get_all_vacancies(self):
        """
        Получает список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
        """
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.company_name, vacancies.vacancy_name, 
                       vacancies.salary_from, vacancies.salary_to, 
                       vacancies.currency, vacancies.vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
            """
            )
            return cur.fetchall()

    def get_avg_salary(self):
        """Получает среднюю зарплату по вакансиям."""
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT AVG((salary_from + salary_to)/2.0)
                FROM vacancies
                WHERE salary_from IS NOT NULL AND salary_to IS NOT NULL
            """
            )
            result = cur.fetchone()
            return result[0] if result else None

    def get_vacancies_with_higher_salary(self):
        """Получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        avg_salary = self.get_avg_salary()
        if avg_salary is None:
            return []

        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.company_name, vacancies.vacancy_name, 
                       vacancies.salary_from, vacancies.salary_to, 
                       vacancies.currency, vacancies.vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE ((vacancies.salary_from + vacancies.salary_to)/2.0) > %s
            """,
                (avg_salary,),
            )
            return cur.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """Получает список всех вакансий, в названии которых содержатся переданные в метод слова, например, python."""
        keyword = f"%{keyword.lower()}%"
        with self.conn.cursor() as cur:
            cur.execute(
                """
                SELECT companies.company_name, vacancies.vacancy_name, 
                       vacancies.salary_from, vacancies.salary_to, 
                       vacancies.currency, vacancies.vacancy_url
                FROM vacancies
                JOIN companies ON vacancies.company_id = companies.company_id
                WHERE LOWER(vacancies.vacancy_name) LIKE %s
            """,
                (keyword,),
            )
            return cur.fetchall()
