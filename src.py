import requests
import psycopg2

class HeadHunterAPI():
    '''Класс для работы с API hh.ru'''

    def get_vacancies(self):
        """Список отслеживаемых компаний и подключение к API hh.ru"""
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
    # Запрос данных для подключения к БД
    print('Укажите данные для подключения к БД:')
    DB_ip_address = input("Введите IP-адрес сервера: (пример - '127.0.0.1')")
    DB_server_name = input("Введите название сервера: (пример - 'vacancies')")
    DB_username = input("Введите имя пользователя: (пример - 'postgres')")
    DB_password = input("Введите пароль: ")

    # Подключение к базе данных
    try:
        conn = psycopg2.connect(host=DB_ip_address, database=DB_server_name, user=DB_username, password=DB_password)
        print("Подключение успешно установлено!")
    except psycopg2.Error as e:
        print("Ошибка подключения к базе данных:", e)
        quit()

    # Открываем курсор для выполнения SQL-запросов
    cursor = conn.cursor()

    # Создаем экземпляр класса
    hh_api = HeadHunterAPI()
    data = hh_api.get_vacancies()

    # Удаление предыдущей таблицы и создание новой перед началом вставки новых данных
    create_table_sql = '''
        CREATE TABLE IF NOT EXISTS vacancies (
            id VARCHAR PRIMARY KEY,
            name VARCHAR,
            area_name VARCHAR,
            salary_from INT,
            salary_to INT,
            published_at TIMESTAMP,
            alternate_url VARCHAR,
            employer_alternate_url VARCHAR,
            snippet_requirement TEXT,
            snippet_responsibility TEXT,
            experience_name VARCHAR,
            employment_name VARCHAR
        );
    '''
    try:
        cursor.execute("drop table vacancies;")
        cursor.execute(create_table_sql)
    finally:
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
