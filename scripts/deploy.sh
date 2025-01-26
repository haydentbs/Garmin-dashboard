#!/bin/bash

# Load environment variables
source .env

# Build and push Docker images
docker build -t garmin-api ./backend
docker build -t garmin-data-pull ./garmin_data_pull

# Tag and push to ECR
aws ecr get-login-password --region $AWS_REGION | docker login --username AWS --password-stdin $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

docker tag garmin-api:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/garmin-api:latest
docker tag garmin-data-pull:latest $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/garmin-data-pull:latest

docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/garmin-api:latest
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/garmin-data-pull:latest

# Update ECS services
aws ecs update-service --cluster garmin-cluster --service garmin-api --force-new-deployment
aws ecs update-service --cluster garmin-cluster --service garmin-data-pull --force-new-deployment