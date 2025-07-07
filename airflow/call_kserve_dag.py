from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime
import requests
import json

# Config
KSERVE_URL = "http://user-persona-recommender.example.com/v1/models/user-persona-recommender:predict"
EMAIL_ALERT_TO = "arpit11103449@gmail.com"

def call_kserve(**context):
    try:
        payload = {
            "instances": [[0.5, 1.2, 3.4, 1, 0, 1]]
        }
        response = requests.post(KSERVE_URL, data=json.dumps(payload), timeout=10)

        if response.status_code != 200:
            raise ValueError(f"KServe returned status {response.status_code}: {response.text}")

        print("Successful prediction:", response.json())

        # Save to XCom for logging or downstream tasks
        context['ti'].xcom_push(key='kserve_response', value=response.json())

    except Exception as e:
        error_msg = f"🔥 KServe call failed: {str(e)}"
        print(error_msg)
        raise Exception(error_msg)

# ✅ Airflow DAG
with DAG(
    dag_id="call_kserve_with_alert",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args={
        "email": [EMAIL_ALERT_TO],
        "email_on_failure": True,
        "email_on_retry": False,
        "retries": 0,
    },
) as dag:

    run_inference = PythonOperator(
        task_id="call_kserve",
        python_callable=call_kserve,
        provide_context=True
    )

    send_failure_email = EmailOperator(
        task_id="send_failure_email",
        to=EMAIL_ALERT_TO,
        subject="🚨 Airflow Alert: KServe Inference Failed",
        html_content="""
            <h3>KServe inference failed</h3>
            <p>Check the Airflow logs for more details.</p>
        """
    )

    # If inference fails, trigger email
    run_inference >> send_failure_email
