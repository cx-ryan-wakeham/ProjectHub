resource "aws_s3_bucket" "projecthub_files" {
  bucket = "projecthub-files-public"
  
  tags = {
    Name = "projecthub-files"
    Environment = var.environment
  }
}

resource "aws_s3_bucket_public_access_block" "projecthub_files" {
  bucket = aws_s3_bucket.projecthub_files.id

  block_public_acls       = false
  block_public_policy     = false
  ignore_public_acls      = false
  restrict_public_buckets = false
}

resource "aws_s3_bucket_policy" "projecthub_files_policy" {
  bucket = aws_s3_bucket.projecthub_files.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Sid    = "PublicReadGetObject"
        Effect = "Allow"
        Principal = "*"
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

resource "aws_s3_bucket" "terraform_state" {
  bucket = "projecthub-terraform-state"
  
  tags = {
    Name = "terraform-state"
  }
}

resource "aws_s3_bucket_cors_configuration" "projecthub_files_cors" {
  bucket = aws_s3_bucket.projecthub_files.id

  cors_rule {
    allowed_headers = ["*"]
    allowed_methods = ["GET", "PUT", "POST", "DELETE", "HEAD"]
    allowed_origins = ["*"]
    expose_headers  = ["ETag"]
    max_age_seconds = 3000
  }
}

