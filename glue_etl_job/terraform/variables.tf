variable "glue_job_name" {
  default = "great_expectation_job"
}

variable "glue_job_description" {
  default = "Data Quality with Great Expectation"
}

variable "glue_job_script_location" {
  default = "cjmm-code-spark"
}

variable "glue_job_schedule_expression" {
  default = "cron(0 0 * * ? *)"
}