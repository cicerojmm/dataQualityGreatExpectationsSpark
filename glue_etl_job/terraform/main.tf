# Criar o job no Glue ETL
resource "aws_glue_job" "glue_etl_job" {
  name         = var.glue_job_name
  description  = var.glue_job_description
  role_arn     = aws_iam_role.glue_etl_role.arn
  glue_version = "3.0"

  worker_type        = "G.1X"
  number_of_workers  = 2

  command {
    name        = "glueetl"
    python_version = "3"
    script_location = "s3://${aws_s3_bucket_object.glue_job_script.bucket}/${aws_s3_bucket_object.glue_job_script.key}"

  }

  default_arguments = {
    "--job-language"     = "python"
    "--additional-python-modules"   = "great_expectations[spark]==0.16.5"
  }

}

# Agendamento do Job do Glue ETL
resource "aws_glue_trigger" "glue_etl_trigger" {
  name            = "daily_etl_trigger"
  description     = "Agendamento diário do GE"
  type            = "SCHEDULED"
  schedule        = var.glue_job_schedule_expression
  start_on_creation = false
  
  actions {
    job_name = aws_glue_job.glue_etl_job.name
  }
}

# Upload do script para o S3
resource "aws_s3_bucket_object" "glue_job_script" {
  bucket = var.glue_job_script_location
  key    = "data_quality/glue_etl/main.py"
  source = "../great_expectation_glue_job.py"
}

# Criar a iam role
resource "aws_iam_policy" "glue_etl_policy" {
  name        = "glue_etl_policy"
  policy      = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect   = "Allow"
        Action   = [
          "s3:GetObject",
          "s3:ListBucket",
          "s3:PutObject",
          "s3:DeleteObject",
          "s3:GetBucketLocation"
        ]
        Resource = [
          "*",
        ]
      }
    ]
  })
}

resource "aws_iam_role" "glue_etl_role" {
  name = "glue_etl_role"
  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "glue.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy_attachment" "glue_etl_attachment" {
  policy_arn = aws_iam_policy.glue_etl_policy.arn
  role       = aws_iam_role.glue_etl_role.name
}
