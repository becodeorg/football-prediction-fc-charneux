# 2. Requirements

This section outlines the functional and non-functional requirements for the Football Match Prediction MVP. These requirements are derived directly from the "Must-have features" defined in the Project Brief, ensuring a focused and achievable scope.

## 2.1. Functional Requirements

*   **FR1**: The system shall display the upcoming 3 Belgian Jupiler Pro League matches on a Streamlit dashboard.
*   **FR2**: The system shall display predicted outcomes for the upcoming 3 matches using a machine learning model on the Streamlit dashboard.
*   **FR3**: The system shall display outcome odds for the upcoming 3 matches on the Streamlit dashboard.
*   **FR4**: The system shall display statistics for each team over their last 5 matches (goals, shots, etc.) on the Streamlit dashboard.
*   **FR5**: The system shall store historical match data in a database (SQLite for MVP).
*   **FR6**: The system shall include a web scraper to fetch recent match data and betting odds.
*   **FR7**: The system shall automate the scraping process using Airflow to periodically update the database.
*   **FR8**: The system shall train a machine learning model on historical match data to predict future match outcomes.
*   **FR9**: The system shall periodically retrain the machine learning model with recent match data and updated statistics.

## 2.2. Non-Functional Requirements

*   **NFR1**: The Streamlit dashboard shall be accessible via a web browser.
*   **NFR2**: The Streamlit dashboard shall load quickly to provide a responsive user experience.
*   **NFR3**: Data updates and model retraining processes shall be efficient.
*   **NFR4**: The system shall use Python for all backend logic, including data processing, ML models, and scraping.
*   **NFR5**: The database shall be SQLite for local development, with consideration for free hosting services for deployment.
*   **NFR6**: The project shall be contained within a single GitHub repository (`football-prediction`).
*   **NFR7**: The system shall have a clear separation of concerns between data engineering and data analysis components.
*   **NFR8**: The system shall ensure seamless data flow from scraped sources to the database, to the ML model, and finally to the Streamlit dashboard.
*   **NFR9**: Basic data security measures shall be in place for the database; no sensitive user data is involved.
