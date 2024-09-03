import psycopg2

from src.config import config
from src.hh_api import get_vacancies, get_companies, get_list_bd
from src.utils import create_db, insert_data
from src.db_man import DBManager


def main():
    """Главная функция для взаимодействия с пользователем"""
    params = config()
    data = get_vacancies(get_companies())
    vac = get_list_bd(data)

    create_db("hh_base", **params)
    conn = psycopg2.connect(dbname="hh_base", **params)
    insert_data(vac, "hh_base", **params)
    manager = DBManager("hh_base", **params)
    print("""
            Здравствуйте! Выберите интересующую вас цифру:
            0 - Выйти из программы.
            1 - Получить список всех компаний и количество вакансий.
            2 - Получить список всех вакансий с указанием названия компании, названия вакансии, зарплаты и ссылки на вакансию.
            3 - Получить среднюю зарплату по вакансиям.
            4 - Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
            5 - Получить список всех вакансий, в названии которых содержатся переданные в метод слова.
        """)

    while True:
        user_input = input()
        if user_input == "1":
            count_comp_and_vac = manager.get_companies_and_vacancies_count()
            print(f"""
            Результат вашего запроса!
            Список всех компаний и количество вакансий: 
            {count_comp_and_vac}.
            """)

        elif user_input == "2":
            count_vacancies = manager.get_all_vacancies()
            print(f"""
            Результат вашего запроса!
            Cписок всех вакансий с указанием названия компании, вакансии, зарплаты и ссылки на вакансию.: 
            {count_vacancies}.
            """)

        elif user_input == "3":
            avg_salary = manager.get_avg_salary()
            print(f"""
            Результат вашего запроса!
            Средняя зарплата по вакансиям: 
            {avg_salary}
            """)

        elif user_input == "4":
            vacancies_with_higher_salary = manager.get_vacancies_with_higher_salary()
            print(f"""
            Результат вашего запроса!
            {vacancies_with_higher_salary}.""")

        elif user_input == "5":
            keyword = input(f'Введите ключевое слово: ').lower()
            vacancies_with_keyword = manager.get_vacancies_with_keyword(keyword)
            print(f"""
            Результат вашего запроса!
            Список всех вакансий, в названии которых содержатся переданные в метод слова 
            {vacancies_with_keyword}""")

        elif user_input == "0":
            print("Завершение работы программы.")
            break


if __name__ == "__main__":
    main()
