# Terraform main configuration with intentional security vulnerabilities

terraform {
  required_version = ">= 0.12"
  
  # VULNERABLE: Backend configuration may expose secrets
  backend "s3" {
    bucket = "projecthub-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
    # VULNERABLE: No encryption, no access control
  }
}

# VULNERABLE: Hardcoded AWS credentials
provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

# VULNERABLE: EC2 instance with excessive permissions
resource "aws_instance" "projecthub_app" {
  ami           = "ami-0c55b159cbfafe1f0"  # VULNERABLE: Outdated AMI
  instance_type = "t2.micro"
  
  # VULNERABLE: Security group allows all traffic
  security_groups = [aws_security_group.projecthub_sg.name]
  
  # VULNERABLE: IAM instance profile with excessive permissions
  iam_instance_profile = aws_iam_instance_profile.projecthub_profile.name
  
  # VULNERABLE: User data with hardcoded secrets
  user_data = <<-EOF
    #!/bin/bash
    export DATABASE_URL="postgresql://projecthub:${var.db_password}@${aws_db_instance.projecthub_db.endpoint}/projecthub"
    export JWT_SECRET="${var.jwt_secret}"
    export AWS_ACCESS_KEY_ID="${var.aws_access_key}"
    export AWS_SECRET_ACCESS_KEY="${var.aws_secret_key}"
  EOF
  
  tags = {
    Name = "projecthub-app"
    Environment = var.environment
  }
}

# VULNERABLE: Security group open to the world
resource "aws_security_group" "projecthub_sg" {
  name        = "projecthub-security-group"
  description = "Security group for ProjectHub"

  # VULNERABLE: Allows all inbound traffic
  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  # VULNERABLE: Allows all outbound traffic
  egress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

  tags = {
    Name = "projecthub-sg"
  }
}

# VULNERABLE: RDS instance with weak configuration
resource "aws_db_instance" "projecthub_db" {
  identifier = "projecthub-db"
  engine     = "postgres"
  engine_version = "10.0"  # VULNERABLE: Outdated PostgreSQL version
  
  instance_class = "db.t2.micro"
  allocated_storage = 20
  
  db_name  = "projecthub"
  username = "projecthub"
  password = var.db_password  # VULNERABLE: Weak password
  
  # VULNERABLE: Publicly accessible database
  publicly_accessible = true
  
  # VULNERABLE: No encryption at rest
  storage_encrypted = false
  
  # VULNERABLE: No backup retention
  backup_retention_period = 0
  
  # VULNERABLE: No deletion protection
  deletion_protection = false
  
  tags = {
    Name = "projecthub-db"
    Environment = var.environment
  }
}

