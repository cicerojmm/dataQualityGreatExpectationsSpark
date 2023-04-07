FROM apache/airflow:2.1.3-python3.8

ARG AIRFLOW_USER_HOME=/opt/airflow/

WORKDIR ${AIRFLOW_USER_HOME}

COPY requirements.txt ${AIRFLOW_USER_HOME}/requirements.txt
RUN pip3 install -r requirements.txt 