from datetime import timedelta
from datetime import datetime
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
import os
import sys

sys.path.append("/home/sol/Desktop/twitch-report")
from get_album import run_spotify_etl
from plugins.get_recomendations import *


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 16),
    'email': ['solbattaglia@gmailcom'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

dag = DAG(
    'spotify_dag',
    default_args=default_args,
    description='Our first DAG with ETL process!',
    schedule_interval=timedelta(days=1),
)



run_etl = PythonOperator(
    task_id='whole_spotify_etl',
    python_callable=run_spotify_etl,
    dag=dag,
)

with DAG('spotify_dag', default_args=default_args, schedule_interval=timedelta(days=1)) as dag:

    get_album = PythonOperator(
        task_id='get_album',
        python_callable=run_spotify_etl,
        provide_context=True
    )

    get_recomendation = PythonOperator(
        task_id='run_spotify_recomendation',
        python_callable=run_spotify_recomendation,
        provide_context=True
    )


    get_album >> get_recomendation