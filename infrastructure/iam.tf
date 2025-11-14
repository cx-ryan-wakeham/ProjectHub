resource "aws_iam_role" "projecthub_role" {
  name = "projecthub-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Action = "sts:AssumeRole"
        Effect = "Allow"
        Principal = {
          Service = "ec2.amazonaws.com"
        }
      }
    ]
  })
}

resource "aws_iam_role_policy" "projecthub_policy" {
  name = "projecthub-policy"
  role = aws_iam_role.projecthub_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "*"
        Resource = "*"
      }
    ]
  })
}

resource "aws_iam_instance_profile" "projecthub_profile" {
  name = "projecthub-profile"
  role = aws_iam_role.projecthub_role.name
}

resource "aws_iam_user" "projecthub_user" {
  name = "projecthub-user"
  
  tags = {
    Name = "projecthub-user"
  }
}

resource "aws_iam_access_key" "projecthub_key" {
  user = aws_iam_user.projecthub_user.name
}

resource "aws_iam_user_policy" "projecthub_user_policy" {
  name = "projecthub-user-policy"
  user = aws_iam_user.projecthub_user.name

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [
      {
        Effect = "Allow"
        Action = "*"
        Resource = "*"
      }
    ]
  })
}

