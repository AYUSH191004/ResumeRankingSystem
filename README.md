# ResumeRankingSystem
This repository contains the code and explanation of an academic group project aimed at automating the resume screening process using Natural Language Processing (NLP) techniques.

## Project Overview
Recruiters often face the challenge of sifting through numerous resumes to find the best candidates for a job opening. This Resume Ranking System streamlines the process by:

* Extracting text from uploaded resumes.

* Analyzing the content using NLP techniques.

* Comparing resumes against a given job description.

* Ranking candidates based on relevance scores.

## Features
* User-Friendly Interface: Simple and intuitive web interface for recruiters.

* Resume Upload: Supports uploading multiple resumes in PDF format.

* Job Description Input: Allows recruiters to input or paste the job description.

* Automated Ranking: Utilizes NLP to rank resumes based on their relevance to the job description.

* Results Display: Presents a ranked list of candidates with their matching scores.

## Recruiter Dashboard

Description: Main interface where recruiters can input job descriptions.![Screenshot 2025-05-17 233146](https://github.com/user-attachments/assets/1f280c5e-e9d1-47f0-8995-04066325efe7)

## Resume Upload

Description: Interface allowing multiple PDF resumes to be uploaded for analysis.![Screenshot 2025-05-17 225101](https://github.com/user-attachments/assets/9311659d-e0f2-46f2-83a6-6bd0f6574cda)

## Ranking Results

Description: Display of ranked resumes with relevance scores.![Screenshot 2025-05-17 233441](https://github.com/user-attachments/assets/d1bcf8da-cc87-4d5b-88fb-5d4758c3b028)


---

## 📦 Technology Stack

### 🎯 Frontend
- **Streamlit**  – For uploading resumes, job descriptions, and viewing rankings

### 🧠 Backend & Core Logic
- **Python** – Core development language.

### 🧾 Resume Parsing & Text Extraction
- **pdfminer.six** / **PyMuPDF** – For PDF parsing
- **python-docx** – For DOCX parsing
- **Regex (`re`)** – Pattern matching and text cleaning

### 🧠 Natural Language Processing (NLP)
- **spaCy / NLTK** – Preprocessing: tokenization, lemmatization, stopword removal
- **Scikit-learn (TF-IDF)** – For converting text to feature vectors
- **Cosine Similarity** – For scoring resume-job relevance

### 🗃️ Database
- **MySQL** – To store parsed resume data, job descriptions, and rankings
- **SQLAlchemy**  – ORM for handling DB interactions

### 🔧 Utilities & Tools
- **Git** – Version control
- **Jupyter Notebook / VS Code** – Development environment

---

## 📈 Outcome
A scalable, AI-based resume screening system that helps recruiters:
- Save time by automatically parsing resumes
- Identify top candidates based on job relevance
- Organize and store candidate data efficiently

---

## 📎 Optional Enhancements
- Add a feedback loop for HRs to improve the ranking algorithm over time
- Integrate email parsing and LinkedIn scraping
- Deploy with CI/CD using Docker and GitHub Actions

---

## 📈 How It Works
* Text Extraction: Extracts text from uploaded PDF resumes.

* Preprocessing: Cleans and preprocesses the text data.

* Feature Extraction: Converts text into numerical features using techniques like TF-IDF.

* Similarity Calculation: Compares resume features with the job description to calculate similarity scores.

* Ranking: Sorts resumes based on their relevance scores.

## Results
* Resume upload sucessfully logs:![Screenshot 2025-05-17 225151](https://github.com/user-attachments/assets/5858bad8-7bef-4e10-9d11-4a72a619960e)
* Job Description saved sucessfully into Database(MYSQL/resume_db)![Screenshot 2025-05-17 231947](https://github.com/user-attachments/assets/bc60828f-a69f-4090-bd3f-5d2a58ae1772)


## 🤝 Contributing
Contributions are welcome! Please fork the repository and submit a pull request for any enhancements or bug fixes.



