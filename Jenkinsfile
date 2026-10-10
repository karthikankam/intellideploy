pipeline {
    agent any

    environment {
        BUILD_TAG = "${env.BUILD_NUMBER}"
        BACKEND_IMAGE  = "intellideploy-backend:${BUILD_TAG}"
        FRONTEND_IMAGE = "intellideploy-frontend:${BUILD_TAG}"
    }

    options {
        timestamps()
        disableConcurrentBuilds()
        buildDiscarder(logRotator(numToKeepStr: '10'))
    }

    stages {

        stage('Checkout') {
            steps {
                checkout scm
            }
        }

        stage('Backend: Install, Train, Test') {
            steps {
                dir('backend') {
                    sh '''
                        python -m venv .venv
                        . .venv/bin/activate
                        pip install --no-cache-dir -r requirements.txt
                        python ml/train_model.py
                        PYTHONPATH=. pytest tests/ --junitxml=test-results.xml
                    '''
                }
            }
            post {
                always {
                    junit 'backend/test-results.xml'
                }
            }
        }

        stage('Frontend: Install & Build') {
            steps {
                dir('frontend') {
                    sh '''
                        npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                sh '''
                    docker build -t $BACKEND_IMAGE ./backend
                    docker build -t $FRONTEND_IMAGE ./frontend
                    docker tag $BACKEND_IMAGE intellideploy-backend:latest
                    docker tag $FRONTEND_IMAGE intellideploy-frontend:latest
                '''
            }
        }

        stage('Deploy') {
            steps {
                sh '''
                    docker compose down --remove-orphans
                    docker compose up -d --build
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                sh '''
                    sleep 10
                    curl -f http://host.docker.internal:8000/health
                    curl -f http://host.docker.internal:8080/
                '''
            }
        }
    }

    post {
        success {
            echo "IntelliDeploy build #${env.BUILD_NUMBER} deployed successfully."
        }
        failure {
            echo "IntelliDeploy build #${env.BUILD_NUMBER} failed - check stage logs above."
        }
        always {
            cleanWs()
        }
    }
}