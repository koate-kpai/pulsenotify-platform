pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Setup and Lint') {
            agent {
                docker { image 'python:3.11-slim' }
            }
            steps {
                sh '''
                    # Create a local virtual environment in the workspace
                    python -m venv venv
                    
                    # Activate it
                    . venv/bin/activate
                    
                    # Install and run (now it has full permissions!)
                    pip install flake8 requests
                    flake8 app
                '''
            }
        }
        
        stage('Containerized Testing') {
            agent {
                docker {
                    image 'docker:cli'
                    // Run as root to allow apk installs, and safely mount the socket
                    args '-u root -v /var/run/docker.sock:/var/run/docker.sock'
                }
            }
            // Set the CI flag so devops.py knows to use host.docker.internal
            environment {
                CI = "true"
            }
            steps {
                sh '''
                    # docker:cli uses Alpine Linux. Install Python and requests first!
                    apk add --no-cache python3 py3-requests
                    
                    # Now we can safely orchestrate the containers
                    python3 devops.py
                ''' 
            }
        }
    }
    
    post {
        always {
            cleanWs()
        }
    }
}