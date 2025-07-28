# 3. Component Breakdown

## 3.1. Data Engineering

-   **Scraper Service (Python)**:
    -   A Python script using libraries like `Playwright` (for dynamic content), `requests` and `BeautifulSoup` (for static content) to scrape betting odds from the specified websites.
    -   This service will be triggered by Airflow.
-   **Database (SQLite)**:
    -   A simple, file-based SQLite database will be used to store the historical match data from the provided CSV and the scraped odds.
    -   This is sufficient for the MVP and requires no external services.
-   **Orchestration (Airflow)**:
    -   Airflow will be used to schedule and automate two main tasks:
        1.  Periodically run the scraper service to get the latest odds.
        2.  Periodically trigger the model retraining process.

## 3.2. Data Science

-   **ML Model (Python)**:
    -   A machine learning model will be developed using libraries like `scikit-learn` or `XGBoost`.
    -   The model will be trained on the historical data and scraped odds to predict match outcomes (Home Win, Draw, Away Win).
-   **Prediction Service (Python)**:
    -   A simple Python function or class that loads the trained model and provides an interface to get predictions for upcoming matches.

## 3.3. Frontend

-   **Streamlit Dashboard (Python)**:
    -   A web-based dashboard built with Streamlit to display:
        -   The next 3 upcoming matches.
        -   The model's prediction for each match.
        -   The scraped betting odds for each match.
        -   Key statistics for the teams involved in the upcoming matches.
