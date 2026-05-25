pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup and Lint') {
            // We tell Jenkins to run these specific steps inside a Python container
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh '''
                    # We are now inside a Python container! No need for a venv.
                    pip install flake8 requests
                    flake8 app
                '''
            }
        }
        
        stage('Containerized Testing') {
            agent {
                docker {
                    image 'docker:cli'
                    // We safely mount the socket ONLY for this specific step
                    args '-v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            steps {
                // We use your custom script to handle the Docker Compose lifecycle!
                sh 'python3 devops.py' 
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}