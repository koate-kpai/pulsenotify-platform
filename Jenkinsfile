pipeline {
    agent any
    
    stages {
        stage('Checkout') {
            steps {
                checkout scm
            }
        }
        
        stage('Environment Setup') {
            steps {
                sh '''
                    # Install requests library needed for devops.py
                    python3 -m venv venv
                    . venv/bin/activate
                    pip install requests
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '''
                    . venv/bin/activate
                    pip install flake8
                    flake8 app
                '''
            }
        }
        
        stage('Containerized Testing') {
            steps {
                // We use your custom script to handle the Docker Compose lifecycle!
                sh '''
                    . venv/bin/activate
                    python3 devops.py
                '''
            }
        }
    }
    
    post {
        always {
            // Safety net: ensure the stack is down even if the script crashes
            sh 'docker compose down -v || true'
            cleanWs()
        }
    }
}