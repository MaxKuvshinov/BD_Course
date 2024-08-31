import psycopg2


class DBManager:
    """Класс, для подключения к БД PostgreSQL"""

    def __init__(self):
        pass

    def get_companies_and_vacancies_count(self):
        """Получение списка всех компаний и количество вакансий у каждой компании."""
        pass

    def get_all_vacancies(self):
        """Получение списка вакансий с указанием названия компании, названия вакансии, зарплаты, ссылки на вакансию"""
        pass

    def get_avg_salary(self):
        """Получение средней зарплаты по вакансиям."""
        pass

    def get_vacancies_with_higher_salary(self):
        """Получение списка всех вакансий, у которых зарплата выше средней по всем вакансиям."""
        pass

    def get_vacancies_with_keyword(self):
        """Получает списка всех вакансий, в названии которых содержатся переданные в метод слова, например python."""
        pass
