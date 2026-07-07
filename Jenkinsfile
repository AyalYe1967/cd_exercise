pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        // שלב 1: הרצת טסטים בסביבת קונטיינר זמנית של פייתון (רצת תמיד ב-Push וב-PR)
        stage('Run Unit Tests in Container') {
            steps {
                script {
                    echo "Running unit tests inside the built container..."
                    
                    // אנחנו מריצים קונטיינר מה-Image שנבנה ודורסים את ה-CMD כדי שיריץ את הטסטים
                    sh "docker run --rm ${IMAGE_NAME}:${IMAGE_TAG} python -m unittest test_app.py"
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