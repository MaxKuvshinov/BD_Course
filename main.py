import psycopg2

from src.config import config
from src.hh_api import get_vacancies, get_companies, get_list_bd
from src.utils import create_db, insert_data
from src.db_man import DBManager


def main():
    # Чтение параметров подключения из файла конфигурации
    params = config()

    # Название базы данных
    database_name = params['dbname']

    # Создание базы данных и таблиц
    create_db(database_name, **params)

    # Получение списка компаний
    companies = get_companies()

    # Получение списка вакансий
    vacancies = get_vacancies(companies)

    # Подготовка данных для вставки в базу данных
    data = get_list_bd(vacancies)

    # Вставка данных в базу данных
    insert_data(data, database_name, **params)

    # Создание экземпляра класса DBManager для работы с базой данных
    db_manager = DBManager(database_name, **params)

    # Выполнение запросов с помощью методов класса DBManager
    print("Компании и количество вакансий:")
    companies_and_vacancies = db_manager.get_companies_and_vacancies_count()
    for company, count in companies_and_vacancies:
        print(f"{company}: {count} вакансий")

    print("\nВсе вакансии:")
    all_vacancies = db_manager.get_all_vacancies()
    for vacancy in all_vacancies:
        print(vacancy)

    print("\nСредняя зарплата по вакансиям:")
    avg_salary = db_manager.get_avg_salary()
    print(f"Средняя зарплата: {avg_salary}")

    print("\nВакансии с зарплатой выше средней:")
    vacancies_with_higher_salary = db_manager.get_vacancies_with_higher_salary()
    for vacancy in vacancies_with_higher_salary:
        print(vacancy)

    print("\nВакансии с ключевым словом 'python':")
    vacancies_with_keyword = db_manager.get_vacancies_with_keyword("python")
    for vacancy in vacancies_with_keyword:
        print(vacancy)


if __name__ == "__main__":
    main()