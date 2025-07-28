# Football Match Prediction Product Requirements Document (PRD)

## 1. Goals and Background Context

### Goals

*   Predict Belgian Jupiler Pro League football match outcomes.
*   Combine historical data with real-time scraped information (odds, recent matches).
*   Present predictions via a Streamlit dashboard.
*   Provide users with data-driven insights and a visual representation of predictions and team statistics.
*   Offer an end-to-end solution for football match prediction, from data ingestion and model training to interactive visualization.
*   Enable users to make informed decisions or simply enjoy data-driven insights into football matches.

### Background Context

The Football Match Prediction project aims to address the complexity of predicting football match outcomes, which often lack real-time data integration, comprehensive team statistics, or an intuitive visualization interface in existing solutions. This project will provide a robust, automated system that combines historical trends with live data to offer more accurate and timely predictions, enhancing user understanding and engagement with football analytics. The solution will leverage web scraping, a machine learning model, and an interactive Streamlit dashboard, with the entire data pipeline automated using Airflow.

### Change Log

| Date       | Version | Description   | Author |
| :--------- | :------ | :------------ | :----- |
| 2025-07-27 | 1.0     | Initial Draft | John   |
| 2025-07-28 | 1.1     | Switched target league to American MLS | Sarah |

## 2. Requirements

This section outlines the functional and non-functional requirements for the Football Match Prediction MVP. These requirements are derived directly from the "Must-have features" defined in the Project Brief, ensuring a focused and achievable scope.

### 2.1. Functional Requirements

*   **FR1**: The system shall display the upcoming 3 Belgian Jupiler Pro League matches on a Streamlit dashboard.
*   **FR2**: The system shall display predicted outcomes for the upcoming 3 matches using a machine learning model on the Streamlit dashboard.
*   **FR3**: The system shall display outcome odds for the upcoming 3 matches on the Streamlit dashboard.
*   **FR4**: The system shall display statistics for each team over their last 5 matches (goals, shots, etc.) on the Streamlit dashboard.
*   **FR5**: The system shall store historical match data in a database (SQLite for MVP).
*   **FR6**: The system shall include a web scraper to fetch recent match data and betting odds.
*   **FR7**: The system shall automate the scraping process using Airflow to periodically update the database.
*   **FR8**: The system shall train a machine learning model on historical match data to predict future match outcomes.
*   **FR9**: The system shall periodically retrain the machine learning model with recent match data and updated statistics.

### 2.2. Non-Functional Requirements

*   **NFR1**: The Streamlit dashboard shall be accessible via a web browser.
*   **NFR2**: The Streamlit dashboard shall load quickly to provide a responsive user experience.
*   **NFR3**: Data updates and model retraining processes shall be efficient.
*   **NFR4**: The system shall use Python for all backend logic, including data processing, ML models, and scraping.
*   **NFR5**: The database shall be SQLite for local development, with consideration for free hosting services for deployment.
*   **NFR6**: The project shall be contained within a single GitHub repository (`football-prediction`).
*   **NFR7**: The system shall have a clear separation of concerns between data engineering and data analysis components.
*   **NFR8**: The system shall ensure seamless data flow from scraped sources to the database, to the ML model, and finally to the Streamlit dashboard.
*   **NFR9**: Basic data security measures shall be in place for the database; no sensitive user data is involved.

## 3. User Interface Design Goals

### 3.1. Overall UX Vision

The overall UX vision is to provide a clear, intuitive, and data-rich experience for football enthusiasts, bettors, and data science students. The dashboard should be easy to navigate, visually appealing, and effectively present complex data in an understandable format. The primary goal is to enable users to quickly grasp match predictions, team performance, and betting odds.

### 3.2. Key Interaction Paradigms

The primary interaction paradigm will be a dashboard-style interface, allowing users to view information at a glance. Interactions will be focused on consuming information, with potential for filtering or sorting upcoming matches if the MVP expands.

### 3.3. Core Screens and Views

From a product perspective, the most critical screens or views necessary to deliver the PRD values and goals are:

*   **Main Dashboard**: This will be the central view displaying upcoming matches, predictions, odds, and team statistics.

### 3.4. Accessibility: None

*Assumption: For the MVP, accessibility will not be a primary focus beyond what Streamlit provides out-of-the-box. This can be revisited in future phases.*

### 3.5. Branding

*Assumption: No specific branding elements or style guides are provided for the MVP. The design will follow a clean, modern aesthetic, leveraging Streamlit's default styling. This can be defined in future phases.*

### 3.6. Target Device and Platforms: Web Responsive

*Assumption: The primary target platform is web, with a responsive design to ensure usability across various screen sizes (desktop, tablet, mobile browsers). No dedicated mobile or desktop applications are planned for the MVP.*

## 4. Technical Assumptions

### 4.1. Repository Structure: Monorepo

*Assumption: A single GitHub repository (`football-prediction`) will contain all code, README, and documentation, as specified in the project brief.*

### 4.2. Service Architecture: Monolith (Python-based)

*Assumption: For the MVP, the system will largely operate as a Python-based monolith, with clear separation of concerns between data engineering (scraping, database, Airflow) and data analysis (ML model, Streamlit app) components. While logically separated, they will reside within the same codebase and deployment unit for simplicity.*

### 4.3. Testing Requirements: Unit + Integration

*Assumption: For the MVP, we will focus on Unit and Integration testing to ensure the correctness of individual components and their interactions. Comprehensive End-to-End (E2E) testing or extensive manual testing will be considered in later phases.*

### 4.4. Additional Technical Assumptions and Requests

*   **Language**: Python will be the sole programming language used across all components (frontend, backend, data processing, ML).
*   **Frontend Framework**: Streamlit will be used for the interactive dashboard.
*   **Data Storage**: SQLite will be used for the database in local development. Consideration for free hosting services (Heroku Postgres, ElephantSQL) for deployment.
*   **Data Scraping Libraries**: `Playwright` (for dynamic content), `requests` and `BeautifulSoup` (for static content) are assumed for web scraping.
*   **ML/Data Science Libraries**: `pandas`, `scikit-learn` (or similar, e.g., `XGBoost`) are assumed for data manipulation and machine learning.
*   **Orchestration**: Apache Airflow will be used for automating the data pipeline.
*   **Deployment**: Deployment strategy for Airflow and Streamlit will be determined by the `dev` and `datadev` agents, but free hosting services are preferred.

## 5. Epic List

Here's a proposed list of epics for the Football Match Prediction project, designed to deliver value incrementally:

*   **Epic 1: Foundation & Data Ingestion**: Establish the core project setup, including the database, initial historical data loading, and the basic web scraping mechanism. This epic will deliver a functional data ingestion pipeline.
    *   *Goal*: To set up the foundational data infrastructure and enable the initial population of the database with historical and scraped data.

*   **Epic 2: Prediction Model & Core Dashboard**: Implement the machine learning model training and prediction service, and integrate it with the Streamlit dashboard to display predictions and basic team statistics.
    *   *Goal*: To deliver the core prediction functionality and an interactive dashboard displaying match outcomes and team data.

*   **Epic 3: Automated Data Pipeline**: Implement Airflow DAGs to automate the periodic scraping of new data and the retraining of the prediction model, ensuring data freshness and model accuracy.
    *   *Goal*: To establish a fully automated and self-sustaining data pipeline for continuous data updates and model improvements.

## 6. Epic 1: Foundation & Data Ingestion

**Expanded Goal:** This epic aims to establish the fundamental data infrastructure for the Football Match Prediction system. This includes setting up the SQLite database, loading the initial historical match data from the provided CSV, and implementing a basic web scraping mechanism to collect real-time betting odds. The successful completion of this epic will provide a robust and continuously updated data foundation for subsequent model training and prediction.

### 6.1. Story 1.1: Database Setup and Historical Data Ingestion

As a **Data Engineer**,
I want to **set up the SQLite database and ingest historical match data**,
so that **the system has a foundational dataset for model training and analysis.**

#### Acceptance Criteria

1.  **1**: The `football.db` SQLite database is created.
2.  **2**: A `matches` table is created within `football.db` with a schema capable of storing all relevant columns from the historical CSV data (Date, Time, HomeTeam, AwayTeam, FTHG, FTAG, FTR, and additional statistics/odds).
3.  **3**: The provided `historical_data.csv` (or equivalent) is successfully loaded into the `matches` table.
4.  **4**: The `db_setup.py` script is executable and idempotent (can be run multiple times without error, replacing existing data if necessary).
5.  **5**: A `.gitignore` entry is added to exclude `football.db` from version control.

### 6.2. Story 1.2: Basic Betting Odds Scraper

As a **Data Engineer**,
I want to **implement a basic web scraper for betting odds**,
so that **the system can collect real-time odds data for upcoming matches.**

#### Acceptance Criteria

1.  **1**: The `scraper.py` script is capable of making HTTP requests to the specified betting odds websites (e.g., WhoScored, SportsGambler, OddsChecker, BetFirst).
2.  **2**: The scraper can extract relevant betting odds (e.g., Home Win, Draw, Away Win odds) for upcoming matches.
3.  **3**: The extracted odds data is structured and can be stored in the `football.db` database, potentially in a new table or by updating existing match records.
4.  **4**: The `scraper.py` script includes basic error handling for network issues or changes in website structure.
5.  **5**: The `scraper.py` script is executable independently for testing purposes.

## 7. Epic 2: Prediction Model & Core Dashboard

**Expanded Goal:** This epic focuses on implementing the core machine learning prediction capabilities and integrating them with the Streamlit dashboard. It will involve training a model on the ingested data, creating a service to provide predictions, and building the user interface to display these predictions along with relevant team statistics.

### 7.1. Story 2.1: ML Model Training and Persistence

As a **Data Analyst**,
I want to **train a machine learning model on historical match data and save it**,
so that **the system can predict future match outcomes.**

#### Acceptance Criteria

1.  **1**: The `model.py` script includes a function `train_model()` that connects to `football.db` and reads the `matches` table.
2.  **2**: The `train_model()` function preprocesses the data (e.g., feature selection, handling categorical variables if necessary) suitable for model training.
3.  **3**: The `train_model()` function trains a machine learning model (e.g., RandomForestClassifier) to predict the `FTR` (Full Time Result).
4.  **4**: The trained model is saved to a file (e.g., `prediction_model.pkl`) in the project root or a designated `models/` directory.
5.  **5**: The `train_model()` function prints the model's accuracy on a test set.
6.  **6**: A `.gitignore` entry is added to exclude `prediction_model.pkl` (or the `models/` directory) from version control.

### 7.2. Story 2.2: Prediction Service Implementation

As a **Data Analyst**,
I want to **implement a function to load the trained model and make predictions**,
so that **the Streamlit app can easily get match outcome predictions.**

#### Acceptance Criteria

1.  **1**: The `model.py` script includes a function `predict_outcome(match_data)` that loads the `prediction_model.pkl`.
2.  **2**: The `predict_outcome()` function takes new match data (e.g., features of an upcoming match) as input.
3.  **3**: The `predict_outcome()` function returns the predicted outcome (H, D, or A) for the given match data.
4.  **4**: The `predict_outcome()` function handles cases where the model file is not found, providing an informative error.

### 7.3. Story 2.3: Streamlit Dashboard - Upcoming Matches & Predictions

As a **Data Analyst**,
I want to **display upcoming matches and their predicted outcomes on the Streamlit dashboard**,
so that **users can quickly see the system's predictions.**

#### Acceptance Criteria

1.  **1**: The `app.py` Streamlit application displays a clear header for "Upcoming Matches".
2.  **2**: The `app.py` connects to `football.db` and retrieves the next 3 upcoming matches (based on date).
3.  **3**: For each upcoming match, the `app.py` calls the `predict_outcome()` function from `model.py` to get the prediction.
4.  **4**: The dashboard clearly displays the home team, away team, and the predicted outcome for each of the 3 upcoming matches.
5.  **5**: The dashboard gracefully handles cases where no upcoming matches are found in the database.

### 7.4. Story 2.4: Streamlit Dashboard - Team Statistics & Odds Display

As a **Data Analyst**,
I want to **display team statistics and betting odds for upcoming matches on the Streamlit dashboard**,
so that **users have comprehensive information for analysis.**

#### Acceptance Criteria

1.  **1**: For each upcoming match, the `app.py` retrieves and displays relevant statistics for both the home and away teams (e.g., goals scored/conceded, shots, etc.) for their last 5 matches.
2.  **2**: The team statistics are presented in a clear and readable format (e.g., a small table or summary).
3.  **3**: The `app.py` retrieves and displays the scraped betting odds for each upcoming match.
4.  **4**: The odds are clearly associated with their respective match and outcome (Home Win, Draw, Away Win).
5.  **5**: The dashboard gracefully handles cases where team statistics or odds are not available.

## 8. Epic 3: Automated Data Pipeline

**Expanded Goal:** This epic aims to establish a fully automated and self-sustaining data pipeline using Apache Airflow. It will ensure that the system continuously collects the latest betting odds and periodically retrains the machine learning model with fresh data, thereby maintaining the accuracy and relevance of the predictions without manual intervention.

### 8.1. Story 3.1: Airflow DAG for Data Scraping

As a **Data Engineer**,
I want to **create an Airflow DAG to automate the execution of the web scraper**,
so that **the betting odds and recent match data are regularly updated in the database.**

#### Acceptance Criteria

1.  **1**: An Airflow DAG file named `scraping_dag.py` is created in the `dags/` directory.
2.  **2**: The `scraping_dag.py` defines a DAG that schedules the execution of the `src/data_engineering/scraper.py` script.
3.  **3**: The DAG is configured to run at a specified frequency (e.g., daily or hourly, to be determined by the team).
4.  **4**: The DAG includes appropriate error handling and logging for the scraping task.
5.  **5**: The DAG successfully triggers the `scraper.py` script, and the scraped data is inserted/updated in the `football.db` database.

### 8.2. Story 3.2: Airflow DAG for Model Retraining

As a **Data Analyst**,
I want to **create an Airflow DAG to automate the retraining of the machine learning model**,
so that **the prediction model remains accurate with the latest data.**

#### Acceptance Criteria

1.  **1**: An Airflow DAG file named `training_dag.py` is created in the `dags/` directory.
2.  **2**: The `training_dag.py` defines a DAG that schedules the execution of the `src/data_analysis/model.py` script's `train_model()` function.
3.  **3**: The DAG is configured to run at a specified frequency (e.g., weekly or after significant data updates).
4.  **4**: The DAG includes appropriate error handling and logging for the model training task.
5.  **5**: The DAG successfully triggers the `train_model()` function, and the `prediction_model.pkl` file is updated with the newly trained model.

## 9. Checklist Results Report

### Category Statuses

| Category                         | Status | Critical Issues |
| :------------------------------- | :----- | :-------------- |
| 1. Problem Definition & Context  | PASS   |                 |
| 2. MVP Scope Definition          | PASS   |                 |
| 3. User Experience Requirements  | PASS   |                 |
| 4. Functional Requirements       | PASS   |                 |
| 5. Non-Functional Requirements   | PASS   |                 |
| 6. Epic & Story Structure        | PASS   |                 |
| 7. Technical Guidance            | PASS   |                 |
| 8. Cross-Functional Requirements | PASS   |                 |
| 9. Clarity & Communication       | PASS   |                 |

### Critical Deficiencies

(None - PRD is considered good by user)

### Recommendations

(None - PRD is considered good by user)

### Final Decision

- **READY FOR ARCHITECT**: The PRD and epics are comprehensive, properly structured, and ready for architectural design.

## 10. Next Steps

### 10.1. UX Expert Prompt

### 10.2. Architect Prompt
