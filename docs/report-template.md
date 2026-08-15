# Deploying a 2-Tier Application on AWS Cloud Using Terraform and Jenkins

## Objective
Deploy a Flask web application on EC2 and a MySQL database on private Amazon RDS. Terraform provisions the infrastructure and Jenkins automates the Terraform workflow.

## Technologies
AWS EC2, Amazon RDS MySQL, VPC, Terraform, Jenkins, Docker, Python Flask, Git and GitHub.

## Architecture
Internet -> EC2/Flask -> private RDS MySQL. The database security group permits port 3306 only from the application security group.

## Evidence
Add your own screenshots for GitHub, Terraform plan/apply, Jenkins, EC2, RDS, the running application, and successful database persistence.

## Conclusion
The project demonstrates infrastructure as code and CI/CD for a basic two-tier cloud application.
