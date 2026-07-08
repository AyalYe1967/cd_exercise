pipeline {
    agent any
    
    environment {
        IMAGE_NAME = 'my-flask-app'
        IMAGE_TAG  = "${env.BUILD_NUMBER}"
        EC2_HOST   = 'YOUR_EC2_IP_OR_DNS'
    }

    stages {
        stage('Build Initial Docker Image') {
            steps {
                script {
                    echo "Building temporary/latest Docker image for testing..."
                    sh "docker build --no-cache -t ${IMAGE_NAME}:latest ."
                }
            }
        }

        stage('Run Unit Tests in Container') {
            steps {
                script {
                    echo "Running unit tests inside the container..."
                    sh "docker run --rm ${IMAGE_NAME}:latest python -m unittest test_app.py"
                }
            }
        }

        stage('Final Build & Tag (PR to Main Only)') {
            when {
                expression { env.CHANGE_ID != null && env.CHANGE_TARGET == 'main' }
            }
            steps {
                script {
                    echo "Pull Request detected targeting 'main'. Tagging official image: ${IMAGE_NAME}:${IMAGE_TAG}..."
                    sh "docker tag ${IMAGE_NAME}:latest ${IMAGE_NAME}:${IMAGE_TAG}"
                }
            }
        }


        stage('Notify GitHub Success') {
            steps {
                script {
                    echo "Notifying GitHub that the build and tests have passed..."
                    step([
                        $class: 'GitHubCommitStatusSetter',
                        reposSource: [$class: 'ManuallyEnteredRepositorySource', url: 'https://github.com/AyalYe1967/cd_exercise'],
                        commitShaSource: [$class: 'ManuallyEnteredShaSource', sha: env.GIT_COMMIT],
                        statusResultSource: [$class: 'ConditionalStatusResultSource', results: [[$class: 'SuccessStatusResult', message: 'Build and Tests Passed!']]]
                    ])
                }
            }
        }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {

            step([
                $class: 'GitHubCommitStatusSetter',
                reposSource: [$class: 'ManuallyEnteredRepositorySource', repo: 'YOUR_GITHUB_USER/YOUR_REPO_NAME'],
                commitShaSource: [$class: 'ManuallyEnteredShaSource', sha: env.GIT_COMMIT],
                statusResultSource: [$class: 'ConditionalStatusResultSource', results: [[$class: 'FailureStatusResult', message: 'Build Failed!']]]
            ])
            echo 'Pipeline failed. Status sent to GitHub as FAILURE.'
        }
    }
}