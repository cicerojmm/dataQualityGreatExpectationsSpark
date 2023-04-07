from datetime import datetime, timedelta
from airflow import DAG
from airflow.providers.amazon.aws.operators.emr_create_job_flow import EmrCreateJobFlowOperator
from airflow.providers.amazon.aws.operators.emr_add_steps import EmrAddStepsOperator
from airflow.contrib.sensors.emr_step_sensor import EmrStepSensor
from airflow.providers.amazon.aws.operators.emr_terminate_job_flow import EmrTerminateJobFlowOperator
from airflow.utils.trigger_rule import TriggerRule
import json
import pathlib

DIR_PATH = pathlib.Path(__file__).parent.absolute()
EMR_CONFIG_PATH = f'{DIR_PATH}/emr_config.json'


def open_conf():
    with open(EMR_CONFIG_PATH) as jsonFile:
        jsonObject = json.load(jsonFile)
    return jsonObject


JOB_FLOW_OVERRIDES = open_conf()

args = str({'job_name': 'process_suite_ge', 'input_path': 's3://cjmm-datalake-raw',
           'output_path': 's3://datadocs-greatexpectations.cjmm'})

STEPS_EMR = [{
    'Name': 'Run Data Quality with Great Expectations',
    'ActionOnFailure': 'CONTINUE',
    'HadoopJarStep': {
            'Jar': 'command-runner.jar',
            'Args': [
                '/usr/bin/spark-submit',
                '--deploy-mode', 'client',
                '--master', 'yarn',
                '--num-executors', '2',
                '--executor-cores', '2',
                '--py-files', 's3://cjmm-code-spark/data_quality/modules.zip',
                's3://cjmm-code-spark/data_quality/main.py', args
            ]
    }
}]

default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': datetime(2023, 4, 5),
    'retries': 1,
    'retry_delay': timedelta(minutes=5)
}

dag = DAG('dag_apply_data_quality_with_ge',
          default_args=default_args,
          description='Run Data Quality with Great Expectations',
          schedule_interval=None)


create_emr = EmrCreateJobFlowOperator(
    task_id='create_emr',
    aws_conn_id='aws_default',
    job_flow_overrides=JOB_FLOW_OVERRIDES,
    dag=dag
)

add_step = EmrAddStepsOperator(
    task_id='add_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr', key='return_value') }}",
    steps=STEPS_EMR,
    dag=dag
)


watch_step = EmrStepSensor(
    task_id='watch_step',
    job_flow_id="{{ task_instance.xcom_pull(task_ids='create_emr', key='return_value') }}",
    step_id="{{ task_instance.xcom_pull('add_step', key='return_value')[0] }}",
    aws_conn_id='aws_default',
    dag=dag,
)

terminate_emr = EmrTerminateJobFlowOperator(
    task_id='terminate_emr',
    job_flow_id="{{ task_instance.xcom_pull('create_emr', key='return_value') }}",
    aws_conn_id='aws_default',
    trigger_rule=TriggerRule.ALL_DONE,
    dag=dag,
)

create_emr >> add_step >> watch_step >> terminate_emr
