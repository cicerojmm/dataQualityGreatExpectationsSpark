from modules.jobs import job_processed_data
from modules.utils.logger_utils import get_logger
from modules.utils.spark_utils import create_spark_session

jobs = {
    'process_suite_ge': job_processed_data.process_suite_ge,
}

def run(parameters):
    logger = get_logger()

    for parameter, value in parameters.items():
        logger.info('Param {param}: {value}'.format(param=parameter, value=value))

    spark = create_spark_session()

    job_name = parameters['job_name']

    process_function = jobs[job_name]
    process_function(
        spark=spark,
        input_path=parameters['input_path'],
        output_path=parameters['output_path']
    )
