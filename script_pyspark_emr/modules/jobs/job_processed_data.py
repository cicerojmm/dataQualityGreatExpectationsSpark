import great_expectations as ge
from great_expectations.core import ExpectationSuite
from great_expectations.core.batch import RuntimeBatchRequest
from great_expectations.core.yaml_handler import YAMLHandler
from great_expectations.validator.validator import Validator
from great_expectations.data_context.types.base import DataContextConfig
from great_expectations.profile.basic_dataset_profiler import BasicDatasetProfiler
from great_expectations.dataset.sparkdf_dataset import SparkDFDataset
from os.path import join

yaml = YAMLHandler()

datasource_yaml = f"""
    name: my_spark_datasource
    class_name: Datasource
    module_name: great_expectations.datasource
    execution_engine:
        module_name: great_expectations.execution_engine
        class_name: SparkDFExecutionEngine
    data_connectors:
        my_runtime_data_connector:
            class_name: RuntimeDataConnector
            batch_identifiers:
                - some_key_maybe_pipeline_stage
                - some_other_key_maybe_airflow_run_id
    """

suite_name = 'suite_tests_amazon_sales_data'
suite_profile_name = 'profile_amazon_sales_data'


def config_data_docs_site(context, output_path):
    data_context_config = DataContextConfig()

    data_context_config["data_docs_sites"] = {
        "s3_site": {
            "class_name": "SiteBuilder",
            "store_backend": {
                "class_name": "TupleS3StoreBackend",
                "bucket": output_path.replace("s3://", "")
            },
            "site_index_builder": {
                "class_name": "DefaultSiteIndexBuilder"
            }
        }
    }

    context._project_config["data_docs_sites"] = data_context_config["data_docs_sites"]


def create_context_ge(output_path):
    context = ge.get_context()

    context.add_expectation_suite(
        expectation_suite_name=suite_name
    )

    context.add_datasource(**yaml.load(datasource_yaml))
    config_data_docs_site(context, output_path)

    return context


def create_validator(context, suite, df):
    runtime_batch_request = RuntimeBatchRequest(
        datasource_name="my_spark_datasource",
        data_connector_name="my_runtime_data_connector",
        data_asset_name="insert_your_data_asset_name_here",
        runtime_parameters={"batch_data": df},
        batch_identifiers={
            "some_key_maybe_pipeline_stage": "ingestion step 1",
            "some_other_key_maybe_airflow_run_id": "run 18",
        },
    )

    df_validator: Validator = context.get_validator(
        batch_request=runtime_batch_request,
        expectation_suite=suite
    )

    return df_validator


def add_tests_suite(df_validator):
    columns_list = ["product_id", "product_name", "category", "discounted_price", "actual_price",
                    "discount_percentage", "rating", "rating_count", "about_product", "user_id",
                    "user_name", "review_id", "review_title", "review_content", "img_link", "product_link"]

    df_validator.expect_table_columns_to_match_ordered_list(columns_list)
    df_validator.expect_column_values_to_be_unique("product_id")
    df_validator.expect_column_values_to_not_be_null("product_id")
    df_validator.expect_column_values_to_be_between(
        column='discount_percentage', min_value=0, max_value=100)
    df_validator.expect_column_values_to_be_between(
        column='rating', min_value=0, max_value=5)
    df_validator.expect_column_values_to_match_regex(
        column="product_link",
        regex=r'^https:\/\/www\.[a-zA-Z0-9\-\.]+\.[a-zA-Z]{2,}$',
        mostly=0.9
    )
    df_validator.save_expectation_suite(discard_failed_expectations=False)

    return df_validator


def add_profile_suite(context, df_ge):
    profiler = BasicDatasetProfiler()
    expectation_suite, validation_result = profiler.profile(df_ge)
    context.save_expectation_suite(expectation_suite, suite_profile_name)


def process_suite_ge(spark, input_path, output_path):
    path_data = join(input_path, 'sales', 'amazon.csv')
    df = spark.read.format("csv").option("header", "true").load(path_data)
    df_ge = SparkDFDataset(df)

    context = create_context_ge(output_path)

    suite: ExpectationSuite = context.get_expectation_suite(
        expectation_suite_name=suite_name)

    add_profile_suite(context, df_ge)

    df_validator = create_validator(context, suite, df)
    df_validator = add_tests_suite(df_validator)

    results = df_validator.validate(expectation_suite=suite)
    context.build_data_docs(site_names=["s3_site"])

    if results['success']:
        print("The test suite run successfully: " +
              str(results['success']))
        print("Validation action if necessary.")
