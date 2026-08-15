variable "aws_region" {
  type    = string
  default = "ap-south-1"
}

variable "project_name" {
  type    = string
  default = "shubham-2tier"
}

variable "key_name" {
  description = "Existing AWS EC2 key pair name"
  type        = string
}

variable "db_password" {
  description = "RDS password"
  type        = string
  sensitive   = true
}

variable "db_username" {
  type    = string
  default = "appuser"
}

variable "db_name" {
  type    = string
  default = "appdb"
}
