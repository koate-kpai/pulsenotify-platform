output "server_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.pulsenotify_test.public_ip
}

output "server_state" {
  description = "The current state of the instance"
  value       = aws_instance.pulsenotify_test.instance_state
}

output "vpc_id" {
  value = module.vpc.vpc_id
}

output "private_subnet_ids" {
  value = module.vpc.private_subnets
}

output "public_subnet_ids" {
  value = module.vpc.public_subnets
}

output "vpc_cidr_block" {
  value = module.vpc.vpc_cidr_block
}