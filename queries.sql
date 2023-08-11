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

SELECT employer_alternate_url, COUNT(*) FROM vacancies GROUP BY employer_alternate_url

SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies

SELECT AVG(CAST(salary_from AS DECIMAL) + CAST(salary_to AS DECIMAL)) / 2 FROM vacancies
            WHERE salary_from > 0 OR salary_to > 0

SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies
            WHERE (salary_from > 0 OR salary_to > 0 )
            AND (CAST(salary_from AS DECIMAL) + CAST(salary_to AS DECIMAL)) / 2 > %s

SELECT employer_alternate_url, name, salary_from, salary_to, alternate_url FROM vacancies
            WHERE LOWER(name) LIKE %s