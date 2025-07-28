# 8. Epic 3: Automated Data Pipeline

**Expanded Goal:** This epic aims to establish a fully automated and self-sustaining data pipeline using Apache Airflow. It will ensure that the system continuously collects the latest betting odds and periodically retrains the machine learning model with fresh data, thereby maintaining the accuracy and relevance of the predictions without manual intervention.

## 8.1. Story 3.1: Airflow DAG for Data Scraping

As a **Data Engineer**,
I want to **create an Airflow DAG to automate the execution of the web scraper**,
so that **the betting odds and recent match data are regularly updated in the database.**

### Acceptance Criteria

1.  **1**: An Airflow DAG file named `scraping_dag.py` is created in the `dags/` directory.
2.  **2**: The `scraping_dag.py` defines a DAG that schedules the execution of the `src/data_engineering/scraper.py` script.
3.  **3**: The DAG is configured to run at a specified frequency (e.g., daily or hourly, to be determined by the team).
4.  **4**: The DAG includes appropriate error handling and logging for the scraping task.
5.  **5**: The DAG successfully triggers the `scraper.py` script, and the scraped data is inserted/updated in the `football.db` database.

## 8.2. Story 3.2: Airflow DAG for Model Retraining

As a **Data Analyst**,
I want to **create an Airflow DAG to automate the retraining of the machine learning model**,
so that **the prediction model remains accurate with the latest data.**

### Acceptance Criteria

1.  **1**: An Airflow DAG file named `training_dag.py` is created in the `dags/` directory.
2.  **2**: The `training_dag.py` defines a DAG that schedules the execution of the `src/data_analysis/model.py` script's `train_model()` function.
3.  **3**: The DAG is configured to run at a specified frequency (e.g., weekly or after significant data updates).
4.  **4**: The DAG includes appropriate error handling and logging for the model training task.
5.  **5**: The DAG successfully triggers the `train_model()` function, and the `prediction_model.pkl` file is updated with the newly trained model.
