module "eks" {
  source  = "terraform-aws-modules/eks/aws"
  version = "19.16.0"
  
  cluster_name    = "pulsenotify-cluster"
  cluster_version = "1.31"
  
  vpc_id                   = module.vpc.vpc_id
  subnet_ids               = module.vpc.private_subnets
  control_plane_subnet_ids = module.vpc.intra_subnets
  
  cluster_endpoint_public_access = true   # So your local kubectl can talk to it
  
  eks_managed_node_groups = {
    pulsenotify_nodes_v2 = {
      min_size     = 1
      max_size     = 3
      desired_size = 2
      instance_types = ["t2.micro"]
      capacity_type  = "ON_DEMAND"   
    }
  }
  
  tags = {
    Environment = "production"
    Project     = "PulseNotify"
  }
}