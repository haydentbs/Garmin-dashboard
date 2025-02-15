provider "aws" {
  region = "us-east-1"  # or your preferred region
}

# VPC and Networking
module "vpc" {
  source = "terraform-aws-modules/vpc/aws"
  
  name = "garmin-vpc"
  cidr = "10.0.0.0/16"
  
  azs             = ["us-east-1a", "us-east-1b"]
  private_subnets = ["10.0.1.0/24", "10.0.2.0/24"]
  public_subnets  = ["10.0.101.0/24", "10.0.102.0/24"]
  
  enable_nat_gateway = true
}

# RDS Instance
resource "aws_db_instance" "garmin_db" {
  identifier        = "garmin-db"
  engine           = "postgres"
  engine_version   = "15"
  instance_class   = "db.t3.micro"
  allocated_storage = 20
  
  db_name          = "garmin"
  username         = "postgres"
  password         = var.db_password  # Define this in variables.tf
  
  vpc_security_group_ids = [aws_security_group.rds_sg.id]
  db_subnet_group_name   = aws_db_subnet_group.garmin.name
}

# ECS Cluster
resource "aws_ecs_cluster" "garmin" {
  name = "garmin-cluster"
}

# ECR Repositories
resource "aws_ecr_repository" "api" {
  name = "garmin-api"
}

resource "aws_ecr_repository" "data_pull" {
  name = "garmin-data-pull"
}