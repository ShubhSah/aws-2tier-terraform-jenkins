pipeline {
    agent any

    environment {
        AWS_DEFAULT_REGION = 'ap-south-1'
        TF_IN_AUTOMATION   = 'true'
    }

    parameters {
        string(
            name: 'KEY_NAME',
            defaultValue: 'aws-2tier-key',
            description: 'Existing EC2 key pair name'
        )

        password(
            name: 'DB_PASSWORD',
            defaultValue: '',
            description: 'RDS database password'
        )
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Terraform Version') {
            steps {
                sh 'terraform --version'
            }
        }

        stage('Terraform Format') {
            steps {
                sh 'terraform -chdir=terraform fmt -check -recursive'
            }
        }

        stage('Terraform Init') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh 'terraform -chdir=terraform init -input=false'
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                sh 'terraform -chdir=terraform validate'
            }
        }

        stage('Terraform Plan') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        terraform -chdir=terraform plan \
                          -input=false \
                          -var="key_name=${KEY_NAME}" \
                          -var="db_password=${DB_PASSWORD}" \
                          -out=tfplan
                    '''
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                input message: 'Apply infrastructure to AWS?', ok: 'Deploy'

                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh 'terraform -chdir=terraform apply -input=false -auto-approve tfplan'
                }
            }
        }

        stage('Application URL') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh 'terraform -chdir=terraform output app_url'
                }
            }
        }
    }

    post {
        always {
            sh 'rm -f terraform/tfplan || true'
        }
    }
}
