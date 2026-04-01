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
                echo '=== Tools Verify kar rahe hain ==='
                sh 'python3 --version'
                sh 'docker --version'
                sh 'ls -la'
            }
        }

        stage('Docker Build') {
            steps {
                echo '=== Docker Image Build ho rahi hai ==='
                sh 'docker build -t ${IMAGE_NAME}:latest .'
                sh 'docker images | grep ${IMAGE_NAME}'
            }
        }

        stage(' Test') {
            steps {
                echo '=== App Test ho rahi hai ==='
                sh '''
                    # Pehle purana test container hata do
                    docker stop test-container || true
                    docker rm   test-container || true

                    # Naya test container run karo
                    docker run -d \
                        --name test-container \
                        -p 5001:5000 \
                        ${IMAGE_NAME}:latest

                    # App start hone ka wait karo
                    sleep 5

                    # Health check karo
                    curl -f http://localhost:5001/health || exit 1
                    echo " Health Check PASSED!"
                '''
            }
        }

        stage('Deploy') {
            steps {
                echo '=== Production Deploy ho raha hai ==='
                sh '''
                    docker stop flask-devops-app || true
                    docker rm flask-devops-app   || true
                    docker-compose down --remove-orphans  || true
                    docker-compose up -d --build
                    sleep 3
                    docker ps | grep flask-devops-app
                    echo " App Successfully Deployed!"
                '''
            }
        }
    }

    post {
        always {
            echo '=== Cleanup ==='
            sh 'docker stop test-container || true'
            sh 'docker rm  test-container || true'
        }
        success {
            echo 'PIPELINE SUCCESS — App live hai http://localhost:5000'
        }
        failure {
            echo ' PIPELINE FAILED — docker logs flask-devops-app check karo'
        }
    }
}
