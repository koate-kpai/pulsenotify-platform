output "server_public_ip" {
  description = "The public IP address of the EC2 instance"
  value       = aws_instance.pulsenotify_test.public_ip
}

output "server_state" {
  description = "The current state of the instance"
  value       = aws_instance.pulsenotify_test.instance_state
}