pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        // שלב 1: בניית הדוקר הראשונית (כדי שתהיה לנו סביבה להריץ עליה טסטים)
        stage('Build Initial Docker Image') {
            steps {
                script {
                    echo "Building temporary/latest Docker image for testing..."
                    sh "docker build --no-cache -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        // שלב 2: הרצת הטסטים מתוך הקונטיינר (רץ תמיד ב-Push וב-PR)
        stage('Run Unit Tests in Container') {
            steps {
                script {
                    echo "Running unit tests inside the container..."
                    sh "docker run --rm ${IMAGE_NAME}:latest python -m unittest test_app.py"
                }
            }
        }

        // שלב 3: תיוג והפקה סופית (רצת אך ורק ב-PR שמכוון ל-main)
        stage('Final Build & Tag (PR to Main Only)') {
            when {
                expression { env.CHANGE_ID != null && env.CHANGE_TARGET == 'main' }
            }
            steps {
                script {
                    echo "Pull Request detected targeting 'main'. Tagging official image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                    // תיוג גרסה ייחודית לפי מספר הריצה בנוסף ל-latest שכבר קיים
                    sh "docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${IMAGE_TAG}"
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