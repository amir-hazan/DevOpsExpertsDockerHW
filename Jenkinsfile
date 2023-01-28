pipeline {
    agent any
    environment {
        DOCKER_REPO = "amirhazan/devops_experts_docker_hw_one"
        COMPOSE_FILE = "docker-compose.yml"
        DB_TAG = "db_app_ver_"
        PY_TAG = "py_app_ver_"
    }
    stages {
        // Checkout to master branch
        stage('checkout') {
            steps {
                script {
                    properties([pipelineTriggers([pollSCM('*/30 * * * *')])])
                }
                git credentialsId: 'githubCredentials', url: 'https://github.com/amir-hazan/DevOpsExpertsDockerHW', branch: 'master'
            }
        }
        // Update env file
        stage('update env file') {
            steps {
                script {
                    bat 'echo "" > proj_envs.env'
                    bat 'echo BUILD_NUMBER=%BUILD_NUMBER% > proj_envs.env'
                    bat 'echo DB_TAG=%DB_TAG% >> proj_envs.env'
                    bat 'echo PY_TAG=%PY_TAG% >> proj_envs.env'
                }
            }
        }
        // Login to docker-hub
        stage('docker hub login') {
            steps {
                script {
                    withCredentials([usernamePassword(credentialsId: 'docker-hub-credentials', passwordVariable: 'HUB_PASS', usernameVariable: 'HUB_USERNAME')]) {
                        bat 'docker login --username "%HUB_USERNAME%" --password "%HUB_PASS%"'
                    }
                }
            }
        }
        // Build docker-compose yml file
        stage('docker-compose build') {
            steps {
                script {
                    bat 'docker-compose --env-file proj_vars/proj_vars.env --file %COMPOSE_FILE% build'
                }
            }
        }
        // Push docker-compose
        stage('docker-compose push') {
            steps {
                script {
                    bat 'docker-compose push'
                }
            }
        }
        // Run docker-compose
        stage('docker-compose run') {
            steps {
                script {
                    bat 'docker-compose --env-file proj_vars/proj_vars.env --file %COMPOSE_FILE% up -d'
                }
            }
        }
    }
    // remove docker images after build and push
    post {
        always {
            bat 'docker-compose --file %COMPOSE_FILE% down --volumes'
            bat 'docker rmi -f %DOCKER_REPO%:%DB_TAG%%BUILD_NUMBER%'
            bat 'docker rmi -f %DOCKER_REPO%:%PY_TAG%%BUILD_NUMBER%'
        }
    }
}
