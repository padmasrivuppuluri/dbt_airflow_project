from airflow.sdk import dag, task
from airflow.operators.bash import BashOperator
from airflow.providers.postgres.hooks.postgres import PostgresHook
import subprocess
from datetime import timedelta


def failure_notification(context):
    dag_id = context["dag"].dag_id
    task_id = context["task_instance"].task_id
    run_id = context["run_id"]

    print("PIPELINE FAILED")
    print(f"DAG: {dag_id}")
    print(f"Task: {task_id}")
    print(f"Run ID: {run_id}")


@dag(
    dag_id="tmdb_ingestion",
    schedule="@daily",
    catchup=False,
    default_args={
        "retries": 3,
        "retry_delay": timedelta(minutes=1),
        "on_failure_callback": failure_notification
    }
)
def tmdb_ingestion():

    @task
    def extract_popular_movies():
        subprocess.run(
            ["python", "/opt/airflow/scripts/tmdb/extract_popular_movies.py"],
            check=True
        )

        return {
            "json_path": "/opt/airflow/include/raw/tmdb/popular_movies.json",
            "source": "tmdb_popular_movies"
        }

    @task
    def load_popular_movies_to_postgres(extract_info):
        print(f"Received from XCom: {extract_info}")

        subprocess.run(
            ["python", "/opt/airflow/scripts/tmdb/load_popular_movies_to_postgres.py"],
            check=True
        )

    @task
    def extract_genres():
        subprocess.run(
            ["python", "/opt/airflow/scripts/tmdb/extract_genres.py"],
            check=True
        )

    @task
    def load_genres_to_postgres():
        subprocess.run(
            ["python", "/opt/airflow/scripts/tmdb/load_genres_to_postgres.py"],
            check=True
        )
    dbt_snapshot = BashOperator(
        task_id="dbt_snapshot",
        bash_command="cd /opt/airflow/dbt/tmdb_dbt && dbt snapshot"
    )

    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command="cd /opt/airflow/dbt/tmdb_dbt && dbt run"
    )

    dbt_test = BashOperator(
        task_id="dbt_test",
        bash_command="cd /opt/airflow/dbt/tmdb_dbt && dbt test"
    )

    extract_task = extract_popular_movies()
    load_task = load_popular_movies_to_postgres(extract_task)
    extract_genres_task = extract_genres()
    load_genres_task = load_genres_to_postgres()
    #validate_task = validate_postgres_load()

    extract_task >> load_task >> extract_genres_task >> load_genres_task >> dbt_snapshot >> dbt_run >> dbt_test


tmdb_ingestion()