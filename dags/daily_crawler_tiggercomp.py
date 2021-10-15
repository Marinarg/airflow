"""
## DAG Documentation
This DAG is responsible for the data ingestion of tiggercomp crawler
"""

import json
from datetime import datetime
from pathlib import Path

from airflow import DAG
from airflow.operators.dummy import DummyOperator
from airflow.operators.bash import BashOperator
from airflow.providers.mysql.operators.mysql import MySqlOperator

with open(str(Path(__file__).resolve().parents[1]) + "/utils/crawlers.json") as json_file:
    json_helper = json.load(json_file)

default_args = {
    "email": "marinarg09@gmail.com",
    "email_on_failure": True,
}
dag = DAG(
        dag_id="tiggercomp_crawler",
        schedule_interval="0 9 * * *",
        start_date=datetime(2021, 1, 1),
        catchup=False,
        default_args=default_args
)

dummy_task = DummyOperator(task_id="dummy_task", dag=dag)

trigger_crawler = BashOperator(
    task_id="trigger_crawler",
    bash_command=json_helper["bash_to_trigger_cralwer"].format("tiggercomp","tiggercomp.csv"),
    dag=dag
)

move_files = BashOperator(
    task_id="move_result_files",
    bash_command=json_helper["bash_to_move_files"].format("tiggercomp.csv"),
    dag=dag
)

insert_csv_on_table_mysql = MySqlOperator(
    task_id="update_mysql_table",
    mysql_conn_id="local_mysql",
    sql=json_helper["sql_to_save_csv"].format("tiggercomp.csv"),
    dag=dag
)

delete_csv_file = BashOperator(
    task_id="delete_csv_file",
    bash_command=json_helper["bash_to_delete_csv"].format("tiggercomp.csv"),
    dag=dag
)

dummy_task >> trigger_crawler >> move_files >> insert_csv_on_table_mysql >> delete_csv_file
