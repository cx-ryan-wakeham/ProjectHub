terraform {
  required_version = ">= 0.12"
  
  backend "s3" {
    bucket = "projecthub-terraform-state"
    key    = "terraform.tfstate"
    region = "us-east-1"
  }
}

provider "aws" {
  region     = var.aws_region
  access_key = var.aws_access_key
  secret_key = var.aws_secret_key
}

resource "aws_instance" "projecthub_app" {
  ami           = "ami-0c55b159cbfafe1f0"
  instance_type = "t2.micro"
  
  security_groups = [aws_security_group.projecthub_sg.name]
  
  iam_instance_profile = aws_iam_instance_profile.projecthub_profile.name
  
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

resource "aws_security_group" "projecthub_sg" {
  name        = "projecthub-security-group"
  description = "Security group for ProjectHub"

  ingress {
    from_port   = 0
    to_port     = 65535
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]
  }

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

resource "aws_db_instance" "projecthub_db" {
  identifier = "projecthub-db"
  engine     = "postgres"
  engine_version = "10.0"
  
  instance_class = "db.t2.micro"
  allocated_storage = 20
  
  db_name  = "projecthub"
  username = "projecthub"
  password = var.db_password
  
  publicly_accessible = true
  
  storage_encrypted = false
  
  backup_retention_period = 0
  
  deletion_protection = false
  
  tags = {
    Name = "projecthub-db"
    Environment = var.environment
  }
}

