pipeline {
    agent any

    environment {
        BUILD_TAG = "${env.BUILD_NUMBER}"
        BACKEND_IMAGE  = "intellideploy-backend:${BUILD_TAG}"
        FRONTEND_IMAGE = "intellideploy-frontend:${BUILD_TAG}"
        DOCKER_HOST = "tcp://localhost:2375"
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
                    bat '''
                        python -m venv .venv
                        call .venv\\Scripts\\activate.bat
                        pip install --no-cache-dir -r requirements.txt
                        python ml\\train_model.py
                        set PYTHONPATH=.
                        pytest tests/ --junitxml=test-results.xml
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
                    bat '''
                        npm install
                        npm run build
                    '''
                }
            }
        }

        stage('Build Docker Images') {
            steps {
                bat """
                    docker build -t %BACKEND_IMAGE% ./backend
                    docker build -t %FRONTEND_IMAGE% ./frontend
                    docker tag %BACKEND_IMAGE% intellideploy-backend:latest
                    docker tag %FRONTEND_IMAGE% intellideploy-frontend:latest
                """
            }
        }

        stage('Deploy') {
            steps {
                bat '''
                    docker compose down --remove-orphans
                    docker compose up -d --build
                '''
            }
        }

        stage('Smoke Test') {
            steps {
                bat '''
                    timeout /t 5
                    curl -f http://localhost:8000/health
                    curl -f http://localhost:8080/
                '''
            }
        }
    }

    post {
        success {
            echo "IntelliDeploy build #${env.BUILD_NUMBER} deployed successfully."
        }
        failure {
            echo "IntelliDeploy build #${env.BUILD_NUMBER} failed — check stage logs above."
        }
        always {
            cleanWs()
        }
    }
}
