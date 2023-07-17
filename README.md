# Data Quality with Great Expectations and Spark

[Great Expectations](https://greatexpectations.io/) is an open-source data validation tool that helps ensure data quality.


### Examples of Architecture


#### Case 1: Great Expectations with Spark on EMR Orchestrated by Airflow
![alt text](https://github.com/cicerojmm/dataQualityGreatExpectationsSpark/blob/main/images/architecture-ge-example1.png?raw=true)


#### Case 2: Great Expectations with Spark on Glue ETL Orchestrated by EventBridge (IaC with Terraform)
![alt text](https://github.com/cicerojmm/dataQualityGreatExpectationsSpark/blob/main/images/architecture-ge-example2.png?raw=true)


### Main projects files
```bash
├───.github
│   ├───workflows
|   |   └───terraform.yml                     # Terraform deploy workflow in AWS for case glue_etl_job
├───airflow
│   ├───airflow_infra
|   |   └───Dockerfile                        # contains some configuration of the Airflow Docker image
|   |   └───docker-compose.yml                # contains the configuration of all Airflow services
|   |   └───requirements.txt                  # contains Python dependencies to run Airflow DAGs
│   ├───dags
│       └───dag_apply_data_quality_with_ge.py # Airflow DAG to create EMR, execute Great Expectations script, and terminate the cluster
|       └───bootstrap-great-expectation.sh    # EMR bootstrap script to install project dependencies
|       └───emr_config.json                   # EMR configuration to run a cluster
├───glue_etl_job
│   ├───terraform            
|   |   └───main.tf                           # services declaration for deploy in AWS: Glue ETL, IAM, S3 and EventBridge
|   |   └───providers.tf                      # configration for deploy in AWS provider
|   |   └───variables.tf                      # declaration variables utilized in Terraform project
|   └───great_expectation_glue_job.py         # main script for execute great expectation in Glue ETL
└───script_pyspark_emr
    ├───modules
    |   └───run.py                            # file responsible for defining which function will be executed
    |   ├───utils
    |   |   └───spark_utils.py                # contains logic to create a Spark instance
    |   |   └───logger_utils.py               # contains logic to manage application logs
    |   ├───jobs
    │       └───job_processed_data.py         # main script with Great Expectations test cases
    └───main.py                               # file that initializes the Spark script execution
```

