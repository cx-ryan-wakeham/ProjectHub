output "ec2_instance_id" {
  description = "EC2 instance ID"
  value       = aws_instance.projecthub_app.id
}

output "ec2_public_ip" {
  description = "EC2 instance public IP"
  value       = aws_instance.projecthub_app.public_ip
}

output "rds_endpoint" {
  description = "RDS instance endpoint"
  value       = aws_db_instance.projecthub_db.endpoint
}

output "rds_password" {
  description = "RDS database password"
  value       = var.db_password
  sensitive   = false
}

output "s3_bucket_name" {
  description = "S3 bucket name"
  value       = aws_s3_bucket.projecthub_files.id
}

output "iam_access_key_id" {
  description = "IAM access key ID"
  value       = aws_iam_access_key.projecthub_key.id
}

output "iam_secret_access_key" {
  description = "IAM secret access key"
  value       = aws_iam_access_key.projecthub_key.secret
  sensitive   = false
}

output "jwt_secret" {
  description = "JWT secret key"
  value       = var.jwt_secret
  sensitive   = false
}

