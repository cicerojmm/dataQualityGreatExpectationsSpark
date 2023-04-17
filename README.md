# Data Quality com Great Expectations e Spark

O [Great Expectations](https://greatexpectations.io/) é uma ferramenta de validação de dados open source que ajuda a garantir a qualidade dos dados.


### Exemplos de arquitetura


#### Case 1: Great Expectations com Spark no EMR Orquestrado pelo Airflow
![alt text](https://github.com/cicerojmm/dataQualityGreatExpectationsSpark/blob/main/images/architecture-ge-simple.png?raw=true)



### Principais arquivos do projeto
```bash
├───airflow
│   ├───airflow_infra
|   |   └───Dockerfile          # contém algumas configurações da imagem Docker do Airflow
|   |   └───docker-compose.yml  # contém a configuração de todos os serviços do Airflow
|   |   └───requirements.txt    # contém as dependências Python para executar as DAGs do Airflow
│   ├───dags
│       └───dag_apply_data_quality_with_ge.py # DAG do Airflow para criar o EMR, executar o script do Great Expectations e terminar o cluster
|       └───bootstrap-great-expectation.sh    # script de bootstrap do EMR para instalação das dependências do projeto
|       └───emr_config.json                   # configuração do EMR para executar um cluster
└───script_pyspark_emr
    ├───modules
    |   └───run.py                            # arquivo responsável por definir qual função será executada
    |   ├───utils
    |   |   └───spark_utils.py                # contém a lógica para criar uma instância do Spark
    |   |   └───logger_utils.py               # contém a lógica para gerenciar os logs da aplicação
    |   ├───jobs
    │       └───job_processed_data.py         # script principal com os case de testes do Great Expectations
    └───main.py                               # arquivo que inicializa a execução do script Spark
```
