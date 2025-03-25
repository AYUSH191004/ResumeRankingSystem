CREATE TABLE candidates (
	candidate_id INTEGER NOT NULL, 
	name VARCHAR(255), 
	email VARCHAR(255), 
	phone VARCHAR(20), 
	linkedin VARCHAR(255), 
	github VARCHAR(255), 
	total_experience FLOAT, 
	highest_qualification VARCHAR(255), 
	university VARCHAR(255), 
	location VARCHAR(255), 
	resume_text TEXT, 
	PRIMARY KEY (candidate_id), 
	UNIQUE (email)
);



CREATE TABLE  skills (
	skill_id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	skill_name VARCHAR(255), 
	proficiency_level VARCHAR(12), 
	PRIMARY KEY (skill_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);

CREATE TABLE projects (
	project_id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	project_title VARCHAR(255), 
	project_description TEXT, 
	technologies_used TEXT, 
	project_url VARCHAR(255), 
	PRIMARY KEY (project_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);

CREATE TABLE work_experience (
	work_id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	company_name VARCHAR(255), 
	job_title VARCHAR(255), 
	start_date DATE, 
	end_date DATE, 
	description TEXT, 
	PRIMARY KEY (work_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);

CREATE TABLE certifications (
	cert_id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	certification_name VARCHAR(255), 
	issuing_organization VARCHAR(255), 
	issue_date DATE, 
	expiration_date DATE, 
	credential_url VARCHAR(255), 
	PRIMARY KEY (cert_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);

CREATE TABLE rankings (
	ranking_id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	skill_score FLOAT, 
	experience_score FLOAT, 
	project_score FLOAT, 
	certification_score FLOAT, 
	overall_score FLOAT, 
	PRIMARY KEY (ranking_id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);

CREATE TABLE analysis_results (
	id INTEGER NOT NULL, 
	candidate_id INTEGER, 
	analysis_date DATETIME, 
	insights TEXT, 
	PRIMARY KEY (id), 
	FOREIGN KEY(candidate_id) REFERENCES candidates (candidate_id)
);
