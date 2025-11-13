# S3 bucket configuration with intentional security vulnerabilities
# VULNERABLE: Public read access
# VULNERABLE: No encryption
# VULNERABLE: Exposed bucket policy

# VULNERABLE: S3 bucket with public access
resource "aws_s3_bucket" "projecthub_files" {
  bucket = "projecthub-files-public"
  
  # VULNERABLE: No versioning
  # VULNERABLE: No encryption
  # VULNERABLE: No lifecycle policies
  
  tags = {
    Name = "projecthub-files"
    Environment = var.environment
  }
}

# VULNERABLE: S3 bucket public access block disabled
resource "aws_s3_bucket_public_access_block" "projecthub_files" {
  bucket = aws_s3_bucket.projecthub_files.id

  block_public_acls       = false  # VULNERABLE: Allows public ACLs
  block_public_policy     = false  # VULNERABLE: Allows public policies
  ignore_public_acls      = false  # VULNERABLE: Doesn't ignore public ACLs
  restrict_public_buckets = false  # VULNERABLE: Doesn't restrict public buckets
}

# VULNERABLE: S3 bucket policy allowing public read access
resource "aws_s3_bucket_policy" "projecthub_files_policy" {
  bucket = aws_s3_bucket.projecthub_files.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "PublicReadGetObject"
        Effect = "Allow"
        Principal = "*"  # VULNERABLE: Allows anyone
        Action = [
          "s3:GetObject",
          "s3:PutObject",
          "s3:DeleteObject"
        ]
        Resource = "${aws_s3_bucket.projecthub_files.arn}/*"
      }
    ]
  })
}

# VULNERABLE: S3 bucket for Terraform state (no encryption)
resource "aws_s3_bucket" "terraform_state" {
  bucket = "projecthub-terraform-state"
  
  # VULNERABLE: No encryption
  # VULNERABLE: No versioning
  # VULNERABLE: Public access not blocked
  
  tags = {
    Name = "terraform-state"
  }
}

# VULNERABLE: S3 bucket CORS configuration allowing all origins
resource "aws_s3_bucket_cors_configuration" "projecthub_files_cors" {
  bucket = aws_s3_bucket.projecthub_files.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["*"]  # VULNERABLE: Allows all origins
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

