from airflow.sdk import dag, task

@dag(
    dag_id="first_dag",
    schedule=None,
    catchup=False
)

def first_dag():
    @task
    def first_task():
        print("This is my first task")
    
    @task
    def second_task():
        print("this is my second task")
    
    first = first_task()
    second = second_task()

    first >> second

first_dag()