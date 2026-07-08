pipeline {
    agent any
    
    environment {
        AWS_REGION      = 'us-east-1' 
        AWS_ACC_ID      = '992382545251' 
        REPOSITORY_NAME = 'a_y/cd'
        IMAGE_TAG       = "v-${env.BUILD_NUMBER}"
        REGISTRY_URL    = "${env.AWS_ACC_ID}.dkr.ecr.${env.AWS_REGION}.amazonaws.com"
    }

    stages {
        stage('Build Initial Docker Image') {
            steps {
                script {
                    echo "Building temporary/latest Docker image for testing..."
                    sh "docker build --no-cache -t ${REPOSITORY_NAME}:latest ."
                }
            }
        }

        stage('Run Unit Tests in Container') {
            steps {
                script {
                    echo "Running unit tests inside the container..."
                    sh "docker run --rm ${REPOSITORY_NAME}:latest python -m unittest test_app.py"
                }
            }
        }

        stage('Push to AWS ECR') {
            when {
                expression { (env.CHANGE_ID != null && env.CHANGE_ID != '') || env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' }
            }
            steps {
                script {
                    echo "Logging in to Amazon ECR..."
                    withCredentials([usernamePassword(credentialsId: 'b6f4c88a-2853-45d6-8a37-eee2bfb73c51', 
                                                      usernameVariable: 'AWS_ACCESS_KEY_ID', 
                                                      passwordVariable: 'AWS_SECRET_ACCESS_KEY')]) {
                        
                        sh "aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REGISTRY_URL}"
                        
                        echo "Tagging image with ${IMAGE_TAG}..."
                        sh "docker tag ${REPOSITORY_NAME}:latest ${REGISTRY_URL}/${REPOSITORY_NAME}:${IMAGE_TAG}"
                        sh "docker tag ${REPOSITORY_NAME}:latest ${REGISTRY_URL}/${REPOSITORY_NAME}:latest"

                        echo "Pushing image to ECR..."
                        sh "docker push ${REGISTRY_URL}/${REPOSITORY_NAME}:${IMAGE_TAG}"
                        sh "docker push ${REGISTRY_URL}/${REPOSITORY_NAME}:latest"
                    }
                }
            }
        }

        stage('Deploy to EC2') {
            when {
                expression { (env.CHANGE_ID != null && env.CHANGE_ID != '') || env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' }
            }
            steps {
                script {
                    echo "Deploying to EC2 server..."
                    
                    def ec2Host = '34.239.116.186'
                    def ec2User = 'ubuntu'            

                    withCredentials([file(credentialsId: 'b7943e0f-cf0c-4a33-8d0f-eda0073045d8', variable: 'SSH_KEY_FILE')]) {
                        sh """
                            chmod 600 \$SSH_KEY_FILE
                            
                            ssh -i \$SSH_KEY_FILE -o StrictHostKeyChecking=no ${ec2User}@${ec2Host} "\
                                aws ecr get-login-password --region ${AWS_REGION} | docker login --username AWS --password-stdin ${REGISTRY_URL} && \
                                docker pull ${REGISTRY_URL}/${REPOSITORY_NAME}:latest && \
                                docker stop my-running-app || true && \
                                docker rm my-running-app || true && \
                                docker run -d --name my-running-app -p 5000:5000 ${REGISTRY_URL}/${REPOSITORY_NAME}:latest \
                            "
                        """
                    }
                }
            }
        }

        stage('Notify GitHub Success') {
            when {
                expression { (env.CHANGE_ID != null && env.CHANGE_ID != '') || env.BRANCH_NAME == 'main' || env.BRANCH_NAME == 'master' }
            }
            steps {
                script {
                    echo "Notifying GitHub that the build and tests have passed..."
                    githubNotify status: 'SUCCESS', description: 'Build, Tests, ECR & Deploy Passed!', context: 'cd_practise_multy'
                }
            }
        }
    }
    
    post {
        success {
            echo 'Pipeline completed successfully!'
        }
        failure {
            script {
                if (env.CHANGE_ID != null && env.CHANGE_ID != '') {
                    githubNotify status: 'FAILURE', description: 'Pipeline Failed!', context: 'cd_practise_multy'
                }
            }
            echo 'Pipeline failed. Status sent to GitHub as FAILURE if applicable.'
        }
    }
}