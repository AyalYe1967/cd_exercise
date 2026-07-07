pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        CONTAINER_NAME = "flask-test-${env.BUILD_NUMBER}"
    }

    stages {
        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Unit Tests in Container') {
            steps {
                script {
                    echo "Running unit tests inside the built docker container..."
                    
                    sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m unittest test_app.py"
                    
                    echo "Unit tests inside container passed successfully!"
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline and Tests completed successfully!'
        }
        failure {
            echo 'Pipeline failed. Cleaning up if needed.'
        }
    }
}