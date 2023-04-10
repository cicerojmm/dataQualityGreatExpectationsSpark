# Data Quality com Great Expectations e Spark

O [Great Expectations](https://greatexpectations.io/) é uma ferramenta de validação de dados open source que ajuda a garantir a qualidade dos dados.


### Exemplos de arquitetura


#### Case 1: Great Expectations com Spark no EMR Orquestrado pelo Airflow
![alt text](https://github.com/cicerojmm/dataQualityGreatExpectationsSpark/blob/main/images/architecture-ge-simple.png?raw=true)



### Principais arquivos do projeto
```
├───airflow
│   ├───airflow_infra: contém a infra do Airflow com Docker e Docker Compose
│   ├───dags
│       └───dag_apply_data_quality_with_ge.py: DAG do Airflow para criar o EMR, executar o script do Great Expectations e terminar o cluster
|       └───bootstrap-great-expectation.sh: script de bootstrap do EMR para instalação das dependências do projeto
|       └───emr_config.json: configuração do EMR para executar um cluster
└───script_pyspark_emr
    ├───modules
    |   ├───jobs
    │       └───job_processed_data.py: script principal com os case de testes do Great Expectations
```
