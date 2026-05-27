terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" {
  region = "us-east-1"
}

resource "aws_instance" "pulsenotify_test" {
  ami           = "ami-00e801948462f718a"
  instance_type = "t3.micro"
  tags = {
    Name    = "Pulsenotify_Test"
    Project = "Pulsenotify"
  }
}