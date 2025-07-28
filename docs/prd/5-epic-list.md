# 5. Epic List

Here's a proposed list of epics for the Football Match Prediction project, designed to deliver value incrementally:

*   **Epic 1: Foundation & Data Ingestion**: Establish the core project setup, including the database, initial historical data loading, and the basic web scraping mechanism. This epic will deliver a functional data ingestion pipeline.
    *   *Goal*: To set up the foundational data infrastructure and enable the initial population of the database with historical and scraped data.

*   **Epic 2: Prediction Model & Core Dashboard**: Implement the machine learning model training and prediction service, and integrate it with the Streamlit dashboard to display predictions and basic team statistics.
    *   *Goal*: To deliver the core prediction functionality and an interactive dashboard displaying match outcomes and team data.

*   **Epic 3: Automated Data Pipeline**: Implement Airflow DAGs to automate the periodic scraping of new data and the retraining of the prediction model, ensuring data freshness and model accuracy.
    *   *Goal*: To establish a fully automated and self-sustaining data pipeline for continuous data updates and model improvements.
