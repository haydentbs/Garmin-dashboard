resource "aws_ecs_service" "api" {
  name            = "garmin-api"
  cluster         = aws_ecs_cluster.garmin.id
  task_definition = aws_ecs_task_definition.api.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.ecs_tasks.id]
  }

  load_balancer {
    target_group_arn = aws_lb_target_group.api.arn
    container_name   = "api"
    container_port   = 5001
  }
}

resource "aws_ecs_service" "data_pull" {
  name            = "garmin-data-pull"
  cluster         = aws_ecs_cluster.garmin.id
  task_definition = aws_ecs_task_definition.data_pull.arn
  desired_count   = 1
  launch_type     = "FARGATE"

  network_configuration {
    subnets         = module.vpc.private_subnets
    security_groups = [aws_security_group.ecs_tasks.id]
  }
}