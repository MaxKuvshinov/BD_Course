import requests


def get_companies():
    """Функция для получения названия компаний по ID"""
    list_companies = {
        'Skyeng': 1122462,
        'Т-Банк': 78638,
        'Вконтакте': 15478,
        'Ozon': 2180,
        'ЦУМ': 52389,
        'Золотое яблоко': 776314,
        'Альфа-Банк': 80,
        'Lamoda': 780654,
        'Газпромбанк': 3388,
        'Сбербанк': 3529
    }

    data = []
    for company_name, company_id in list_companies.items():
        company_url = f'https://hh.ru/employer/{company_id}'
        company_info = {'company_id': company_id, 'company_name': company_name, 'company_url': company_url}
        data.append(company_info)

    return data


def get_vacancies(data):
    """Функция для получения данных о компаниях и вакансиях"""

    list_vacancy = []

    for company in data:
        company_id = company['company_id']
        url = f"https://api.hh.ru/vacancies?employer_id={company_id}"
        response = requests.get(url)
        if response.status_code == 200:
            vacancy = response.json().get('items', [])
            list_vacancy.extend(vacancy)
        else:
            print(f'Ошибка: {response.status_code} для компании ID {company_id}')

    return list_vacancy


def get_list_bd(vacancies):
    """Функция для преобразования данных для БД"""
    result = []
    for item in vacancies:
        company_name = item['employer']['name']
        company_id = item['employer']['id']
        company_url = item['employer']['url']
        vacancy_name = item['name']
        vacancy_url = item['alternate_url']
        salary = item.get('salary')
        salary_from = 0
        salary_to = 0
        currency = " "
        description = item["snippet"].get("responsibility", " ")
        experience = item["experience"]["name"]
        requirement = item['snippet'].get('requirement', " ")

        if salary:
            salary_from = salary.get("from", 0)
            salary_to = salary.get("to", 0)
            currency = salary.get("currency", " ")

        result.append(
            {
                'company_id': company_id,
                'company_name': company_name,
                'company_url': company_url,
                'vacancy_name': vacancy_name,
                'vacancy_url': vacancy_url,
                'salary_from': salary_from,
                'salary_to': salary_to,
                'currency': currency,
                'description': description,
                'experience': experience,
                'requirement': requirement
            }
        )
    return result


# comp = get_companies()
# vac = get_vacancies(comp)
# vacancies_list = get_list_bd(vac)
# print(vacancies_list)




