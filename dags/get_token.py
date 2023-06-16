import requests
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable
from datetime import datetime, timedelta
# from airflow.secrets import get_secret


def SpotifyToken():
    client_id = Variable.get('spotify_client_id')
    client_secret = Variable.get('spotify_client_secret')
    auth_url = 'https://accounts.spotify.com/api/token'

    auth_response = requests.post(auth_url, {
        'grant_type': 'client_credentials',
        'client_id': client_id,
        'client_secret': client_secret,
    })

    auth_response_data = auth_response.json()

    return auth_response_data['access_token']

def StoreToken(**kwargs):
    token = kwargs['ti'].xcom_pull(task_ids='get_token')
    Variable.set("spotify_token", token)

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 6, 16),
    'email': ['airflow@example.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

with DAG('get_token', default_args=default_args, schedule_interval=timedelta(hours=1.5)) as dag:

    get_token = PythonOperator(
        task_id='get_token',
        python_callable=SpotifyToken,
        provide_context=True
    )

    store_token = PythonOperator(
        task_id='store_token',
        python_callable=StoreToken,
        provide_context=True
    )

    get_token >> store_token
