from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def _retrain_model_task():
    # Import and call the train_model function from src.modeling.model
    # Example: from src.modeling.model import train_model
    # train_model()
    print("Retraining model task...")

with DAG(
    dag_id='football_training_dag',
    start_date=datetime(2023, 1, 1),
    schedule_interval='@weekly', # Example schedule
    catchup=False
) as dag:
    train_task = PythonOperator(
        task_id='retrain_model',
        python_callable=_retrain_model_task
    )