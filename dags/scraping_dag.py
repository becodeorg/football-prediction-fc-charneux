from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _run_scraper_task():
    # Import and call the scraper function from src.data_collection.scraper
    # Example: from src.data_collection.scraper import run_scraper
    # run_scraper()
    print("Running scraping task...")

with DAG(
    dag_id='football_scraping_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@daily', # Example schedule
    catchup=False
) as dag:
    scrape_task = PythonOperator(
        task_id='run_scraper',
        python_callable=_run_scraper_task
    )