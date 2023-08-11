from src import HeadHunterAPI, save_to_bd
from BD_manager import DBManager


if __name__ == "__main__":
    print("""1. Показать список отслеживаемых компаний:
2. Выгрузить актуальную информацию о вакансиях в БД
3. Фильтрация вакансий в БД
0. Выйти.""")
    choice = input("Выберите действие: ")
    while choice != '0' or '3':
        if choice == '1':
            print("Сбербанк-Сервис, МТС, Альфа-Банк, VK, Ozon, Яндекс, Билайн, Ventra, Авито, Rambler")
            choice = input("Выберите действие: ")
        elif choice == '2':
            save_to_bd()
            print("Данные выгружены в БД")
            choice = input("Выберите действие: ")
        elif choice == '3':
            print("""1. Получить список всех компаний и количество вакансий у каждой компании.
2. Получить список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию.
3. Получить среднюю зарплату по вакансиям.
4. Получить список всех вакансий, у которых зарплата выше средней по всем вакансиям.
5. Получить список вакансий по ключевому слову.
0. Выйти. """)
            choice_two = input("Выберите действие: ")
            if choice_two == '1':
                db_manager = DBManager()
                print(db_manager.get_companies_and_vacancies_count())
            elif choice_two == '2':
                db_manager = DBManager()
                print(db_manager.get_all_vacancies())
            elif choice_two == '3':
                db_manager = DBManager()
                print(round(db_manager.get_avg_salary(), 1))
            elif choice_two == '4':
                db_manager = DBManager()
                count = round(db_manager.get_avg_salary(), 1)
                print(db_manager.get_vacancies_with_higher_salary(count))
            elif choice_two == '5':
                keyword = input("Введите ключевое слово для поиска: ")
                db_manager = DBManager()
                print(db_manager.get_vacancies_with_keyword(keyword))
            elif choice_two == '0':
                quit()
        elif choice == '0':
            quit()
        else:
            print("Неверный выбор.")