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