pipeline {
    agent any

    environment {
        DOCKER_CREDENTIALS_ID = 'dockerhub_credentials'  // Your Jenkins Docker Hub credentials ID
        GIT_REPO_URL = 'https://github.com/vassgps/webapp.git'
        DOCKERHUB_REPO = 'vassgps/webapp'
        DOCKERHUB_TAG = 'develop'  // Change to appropriate tag based on branch
        PROJECT_DIR = 'webapp'  // The directory containing your docker-compose.yml file
        LOG_FILE = 'pipeline_log.txt'
    }

    stages {
        stage('Checkout Code') {
            steps {
                echo "Checking out code from GitHub..."
                git branch: 'develop', url: env.GIT_REPO_URL
                echo "Code checked out successfully."
            }
            post {
                success {
                    echo "Checkout completed successfully."
                }
                failure {
                    echo "Checkout failed. Please check the repository URL and branch name."
                }
            }
        }

        stage('Build Docker Image') {
            steps {
                script {
                    echo "Building Docker image..."
                    dir(env.PROJECT_DIR) {
                        sh "docker build -t ${env.DOCKERHUB_REPO}:${env.DOCKERHUB_TAG} -f app/Dockerfile . 2>&1 | tee ${env.LOG_FILE}"
                    }
                    echo "Docker image built successfully."
                }
            }
            post {
                success {
                    echo "Docker image built and tagged successfully."
                }
                failure {
                    echo "Docker build failed. Please check the Dockerfile and the build logs."
                    archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
                }
            }
        }


        stage('Push Docker Image') {
            steps {
                script {
                    echo "Pushing Docker image to Docker Hub..."
                    docker.withRegistry('https://index.docker.io/v1/', env.DOCKER_CREDENTIALS_ID) {
                        sh "docker push ${env.DOCKERHUB_REPO}:${env.DOCKERHUB_TAG} 2>&1 | tee -a ${env.LOG_FILE}"
                    }
                    echo "Docker image pushed successfully to Docker Hub."
                }
            }
            post {
                success {
                    echo "Docker image pushed to Docker Hub successfully."
                }
                failure {
                    echo "Failed to push Docker image to Docker Hub. Please check the Docker Hub credentials and repository."
                    archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
                }
            }
        }

        stage('Deploy on AWS LightSail') {
            steps {
                script {
                    echo "Deploying Docker containers on AWS LightSail..."
                    dir(env.PROJECT_DIR) {
                        sh """
                        docker-compose down
                        docker-compose pull
                        docker-compose up -d 2>&1 | tee -a ${env.LOG_FILE}
                        """
                    }
                    echo "Deployment on AWS LightSail completed successfully."
                }
            }
            post {
                success {
                    echo "Deployment completed successfully."
                }
                failure {
                    echo "Deployment failed. Please check the docker-compose.yml file and the logs."
                    archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
                }
            }
        }
    }

    post {
        always {
            echo "Cleaning up unused Docker images..."
            sh "docker image prune -f 2>&1 | tee -a ${env.LOG_FILE}"
            archiveArtifacts artifacts: env.LOG_FILE, allowEmptyArchive: true
            echo "Pipeline finished."
        }
    }
}
