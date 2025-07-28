# 4. Technical Assumptions

## 4.1. Repository Structure: Monorepo

*Assumption: A single GitHub repository (`football-prediction`) will contain all code, README, and documentation, as specified in the project brief.*

## 4.2. Service Architecture: Monolith (Python-based)

*Assumption: For the MVP, the system will largely operate as a Python-based monolith, with clear separation of concerns between data engineering (scraping, database, Airflow) and data analysis (ML model, Streamlit app) components. While logically separated, they will reside within the same codebase and deployment unit for simplicity.*

## 4.3. Testing Requirements: Unit + Integration

*Assumption: For the MVP, we will focus on Unit and Integration testing to ensure the correctness of individual components and their interactions. Comprehensive End-to-End (E2E) testing or extensive manual testing will be considered in later phases.*

## 4.4. Additional Technical Assumptions and Requests

*   **Language**: Python will be the sole programming language used across all components (frontend, backend, data processing, ML).
*   **Frontend Framework**: Streamlit will be used for the interactive dashboard.
*   **Data Storage**: SQLite will be used for the database in local development. Consideration for free hosting services (Heroku Postgres, ElephantSQL) for deployment.
*   **Data Scraping Libraries**: `Playwright` (for dynamic content), `requests` and `BeautifulSoup` (for static content) are assumed for web scraping.
*   **ML/Data Science Libraries**: `pandas`, `scikit-learn` (or similar, e.g., `XGBoost`) are assumed for data manipulation and machine learning.
*   **Orchestration**: Apache Airflow will be used for automating the data pipeline.
*   **Deployment**: Deployment strategy for Airflow and Streamlit will be determined by the `dev` and `datadev` agents, but free hosting services are preferred.
