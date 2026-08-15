# AWS 2-Tier Application with Terraform + Jenkins

Original learning project: Flask on EC2 + MySQL on private RDS, provisioned by Terraform and automated with Jenkins.

Architecture: Internet -> EC2/Flask -> private RDS MySQL

## Prerequisites
- AWS account
- Terraform >= 1.6
- Jenkins Linux agent with Terraform and AWS CLI
- Git
- Docker
- Existing EC2 key pair

## Local deployment
```bash
cd terraform
terraform init
terraform fmt -recursive
terraform validate
terraform plan -var="key_name=YOUR_KEYPAIR" -var="db_password=YOUR_STRONG_PASSWORD"
terraform apply -var="key_name=YOUR_KEYPAIR" -var="db_password=YOUR_STRONG_PASSWORD"
terraform output app_url
```

## Jenkins
Create a Pipeline from this repository. Configure AWS credentials securely on the Jenkins agent. The Jenkinsfile validates Terraform, creates a plan, asks for approval, and applies it.

## Cleanup
```bash
cd terraform
terraform destroy -var="key_name=YOUR_KEYPAIR" -var="db_password=YOUR_STRONG_PASSWORD"
```

Never commit credentials, passwords, private keys, or Terraform state. Use your own screenshots and deployment evidence for an assignment.
