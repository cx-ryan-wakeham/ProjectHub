variable "aws_region" {
  description = "AWS region"
  default     = "us-east-1"
}

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
}

variable "jwt_secret" {
  description = "JWT secret key"
  default     = "secret_key_12345"
}

variable "environment" {
  description = "Environment name"
  default     = "production"
}

