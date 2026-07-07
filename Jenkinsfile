pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        // שלב 1: הרצת טסטים בסביבת קונטיינר זמנית של פייתון (רצת תמיד ב-Push וב-PR)
        stage('Run Unit Tests') {
            steps {
                script {
                    echo "Running unit tests using Jenkins WORKSPACE: ${env.WORKSPACE}"
                    
                    sh """
                        docker run --rm -v ${env.WORKSPACE}:/app -w /app python:3.11-slim bash -c "
                            echo 'Checking files inside container:'
                            ls -la
                            pip install --upgrade pip
                            if [ -f requirements.txt ]; then pip install -r requirements.txt; fi
                            python -m unittest test_app.py
                        "
                    """
                }
            }
        }

        // שלב 2: בניית הדוקר רק ב-PR ל-main (כפי שהגדרנו קודם)
        stage('Build Docker Image (PR to Main Only)') {
            when {
                expression { env.CHANGE_ID != null && env.CHANGE_TARGET == 'main' }
            }
            steps {
                script {
                    echo "Building Docker image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                    sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            echo 'Pipeline failed.'
        }
    }
}