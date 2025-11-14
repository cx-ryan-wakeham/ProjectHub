# Terraform variables with intentional security vulnerabilities

variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

# : Hardcoded credentials in variables
variable "aws_access_key" {
  description = "AWS Access Key"
  default     = "AKIAIOSFODNN7EXAMPLE"
}

variable "aws_secret_key" {
  description = "AWS Secret Key"
  default     = "wJalrXUtnFEMI/K7MDENG/bPxRfiCYEXAMPLEKEY"
}

variable "db_password" {
  description = "Database password"
  default     = "password123"
  # : Password in plain text
}

variable "jwt_secret" {
  description = "JWT secret key"
  default     = "secret_key_12345"
  # : Secret in plain text
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

