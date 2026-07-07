pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}" 
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."

                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                    
                    echo "Docker image built successfully!"
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline build stage completed successfully.'
        }
        failure {
            echo 'Pipeline build stage failed.'
        }
    }
}