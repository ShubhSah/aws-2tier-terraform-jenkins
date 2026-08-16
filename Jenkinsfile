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

        stage('Test AWS Access') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        aws sts get-caller-identity
                        aws s3 ls s3://shubham-2tier-tfstate-618257309226/aws-2tier/
                    '''
                }
            }
        }

        stage('Terraform Format') {
            steps {
                sh '''
                    cd terraform
                    terraform fmt -check -recursive
                '''
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
                    sh '''
                        cd terraform
                        terraform init -input=false
                    '''
                }
            }
        }

        stage('Terraform Validate') {
            steps {
                sh '''
                    cd terraform
                    terraform validate
                '''
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
                        cd terraform

                        terraform plan \
                            -input=false \
                            -out=tfplan \
                            -var="key_name=${KEY_NAME}" \
                            -var="db_password=${DB_PASSWORD}"
                    '''
                }
            }
        }

        stage('Terraform Apply') {
            steps {
                input(
                    message: 'Apply infrastructure to AWS?',
                    ok: 'Deploy'
                )

                withCredentials([
                    usernamePassword(
                        credentialsId: 'aws-credentials',
                        usernameVariable: 'AWS_ACCESS_KEY_ID',
                        passwordVariable: 'AWS_SECRET_ACCESS_KEY'
                    )
                ]) {
                    sh '''
                        cd terraform

                        terraform apply \
                            -input=false \
                            -auto-approve \
                            tfplan
                    '''
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
                    sh '''
                        cd terraform

                        echo "======================================"
                        echo "      AWS 2-TIER APPLICATION URL"
                        echo "======================================"

                        terraform output app_url

                        echo "======================================"
                        echo "         APPLICATION DETAILS"
                        echo "======================================"

                        terraform output app_public_ip
                        terraform output db_endpoint
                    '''
                }
            }
        }
    }

    post {
        always {
            sh 'rm -f terraform/tfplan'
        }

        success {
            echo 'AWS 2-Tier deployment completed successfully!'
        }

        failure {
            echo 'AWS 2-Tier deployment failed. Check the console output.'
        }
    }
}
