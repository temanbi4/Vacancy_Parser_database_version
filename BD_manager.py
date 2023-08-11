import psycopg2
class DBManager:
    """класс для подключения к БД"""
    def __init__(self):
        self.conn = psycopg2.connect(host='127.0.0.1', database='vacancies', user='postgres', password='369369')
        self.cursor = self.conn.cursor()

    def get_companies_and_vacancies_count(self):
        """получает список всех компаний и количество вакансий у каждой компании."""

        self.cursor.execute("""
            SELECT employer_alternate_url, COUNT(*) FROM vacancies GROUP BY employer_alternate_url;
        """)
        return self.cursor.fetchall()

    def get_all_vacancies(self):
        """получает список всех вакансий с указанием названия компании, названия вакансии и зарплаты и ссылки на вакансию."""

        self.cursor.execute("""
            SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies;
        """)
        return self.cursor.fetchall()

    def get_avg_salary(self):
        """получает среднюю зарплату по вакансиям."""

        self.cursor.execute("""
            SELECT AVG(CAST(salary_from AS DECIMAL) + CAST(salary_to AS DECIMAL)) / 2 FROM vacancies 
            WHERE salary_from > 0 OR salary_to > 0;
        """)
        return self.cursor.fetchone()[0]

    def get_vacancies_with_higher_salary(self, avg_salary):
        """получает список всех вакансий, у которых зарплата выше средней по всем вакансиям."""

        self.cursor.execute("""
            SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies 
            WHERE (salary_from > 0 OR salary_to > 0 ) 
            AND (CAST(salary_from AS DECIMAL) + CAST(salary_to AS DECIMAL)) / 2 > %s;
        """, (avg_salary,))
        return self.cursor.fetchall()

    def get_vacancies_with_keyword(self, keyword):
        """получает список всех вакансий c ключевым словом"""
        self.cursor.execute("""
            SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies 
            WHERE LOWER(name) LIKE %s;
        """, ('%' + keyword.lower() + '%',))
        return self.cursor.fetchall()



