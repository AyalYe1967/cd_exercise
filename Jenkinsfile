pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
    }

    stages {
        stage('Run Unit Tests') {
            steps {
                script {
                    echo "Running unit tests..."
                    sh "python3 -m unittest test_app.py"
                }
            }
        }

        stage('Build & Deploy (Main / Specific Branch Only)') {
            steps {
                script {
                    // בדיקה האם אנחנו רצים על בראנץ' main (או בראנץ' ספציפי אחר שמותר לו לבנות דוקר)
                    // env.BRANCH_NAME או env.GIT_BRANCH תלוי איך הגדרת את המשיכה מגיטהאב
                    def currentBranch = env.BRANCH_NAME ?: env.GIT_BRANCH ?: "unknown"
                    
                    // נקה את שם הבראנץ' אם הוא מגיע בצורה כמו origin/main
                    if (currentBranch.contains('main')) {
                        echo "Target branch is main. Building Docker image..."
                        sh "docker build -t ${IMAGE_NAME}:${IMAGE_TAG} -t ${IMAGE_NAME}:latest ."
                    } else {
                        echo "Current branch is '${currentBranch}', skipping Docker build."
                    }
                }
            }
        }
    }
}