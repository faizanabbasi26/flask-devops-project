pipeline {
    agent any

    environment {
        IMAGE_NAME = 'flask-devops-app'
    }

    stages {
        stage('Code Checkout') {
            steps {
                echo '=== GitHub se Code Checkout ==='
                checkout scm
            }
        }

        stage('Environment Verify') {
            steps {
                sh 'python3 --version'
                sh 'docker --version'
            }
        }

        stage('Docker Build') {
            steps {
                sh 'docker build -t ${IMAGE_NAME}:latest .'
            }
        }

        stage('Test') {
            steps {
                sh '''
                    docker stop test-container || true
                    docker rm test-container || true
                    docker run -d --name test-container -p 5001:5000 ${IMAGE_NAME}:latest
                    sleep 5
                    curl -f http://localhost:5001/health || exit 1
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker stop flask-devops-app || true
                    docker rm flask-devops-app || true
                    docker run -d --name flask-devops-app -p 5000:5000 ${IMAGE_NAME}:latest
                    sleep 3
                    docker ps | grep flask-devops-app
                '''
            }
        }
    }

    post {
        always {
            sh 'docker stop test-container || true'
            sh 'docker rm test-container || true'
        }
        success {
            echo 'PIPELINE SUCCESS!'
        }
        failure {
            echo 'PIPELINE FAILED!'
        }
    }
}
