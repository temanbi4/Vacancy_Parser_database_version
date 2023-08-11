import requests
import psycopg2

class HeadHunterAPI():
    '''Класс для работы с API hh.ru'''

    def get_vacancies(self):

        selected_id_companies = {
            'Сбербанк-Сервис': 1473866,
            'МТС': 3776,
            'Альфа-Банк': 80,
            'VK': 15478,
            'Ozon': 2180,
            'Яндекс': 1740,
            'Билайн': 4934,
            'Ventra': 1838,
            'Авито': 84585,
            'Rambler': 8620
        }

        data = []

        for k, v in selected_id_companies.items():
            url = f'https://api.hh.ru/vacancies?employer_id={v}'
            response = requests.get(url).json()
            data.extend(response['items'])
        return data

def save_to_bd():
    # Подключение к базе данных
    conn = psycopg2.connect(host='127.0.0.1', database='vacancies', user='postgres', password='369369')

    # Открываем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Создаем экземпляр класса
    hh_api = HeadHunterAPI()
    data = hh_api.get_vacancies()

    # Очистка таблицы перед началом вставки новых данных
    cursor.execute("DELETE FROM vacancies;")
    conn.commit()

    # Перебираем каждый элемент данных и сохраняем его в базе данных
    for item in data:
        try:
            salary_from = item['salary']['from'] if item['salary'] is not None and 'from' in item['salary'] else 0
            salary_to = item['salary']['to'] if item['salary'] is not None and 'to' in item['salary'] else 0

            cursor.execute("""
                    INSERT INTO vacancies (id, name, area_name, salary_from, salary_to, published_at, alternate_url, employer_alternate_url, snippet_requirement, snippet_responsibility, experience_name, employment_name)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s);
                """, (
                item['id'],
                item['name'],
                item['area']['name'],
                salary_from,
                salary_to,
                item['published_at'],
                item['alternate_url'],
                item['employer']['alternate_url'],
                item['snippet']['requirement'],
                item['snippet']['responsibility'],
                item['experience']['name'],
                item['employment']['name']
            ))
            conn.commit()

        except (KeyError, IndexError) as e:
            print(f"Ошибка при обработке записи: {e}")
            conn.rollback()

    cursor.close()
    conn.close()
