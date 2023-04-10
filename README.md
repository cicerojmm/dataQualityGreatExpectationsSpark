# Data Quality com Great Expectations e Spark

O [Great Expectations](https://greatexpectations.io/) é uma ferramenta de validação de dados open source que ajuda a garantir a qualidade dos dados.

### Exemplos de arquitetura
#### Case 1: Great Expectations com Spark no EMR Orquestrado pelo Airflow
![alt text](https://github.com/cicerojmm/dataQualityGreatExpectationsSpark/blob/main/images/architecture-ge-simple.png?raw=true)


### Esquema de diretórios

├───airflow
│   ├───airflow_infra
│   ├───dags
│       └───dag_apply_data_quality_with_ge.py
|       └───bootstrap-great-expectation.sh
|       └───emr_config.json
└───script_pyspark_emr
    ├───modules
    |   ├───jobs
    │       └───job_processed_data.py
