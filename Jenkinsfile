pipeline {
    agent any
     environment {
        IMAGE_NAME = "yasmine650/jenkins-flask-app"
        IMAGE_TAG = "${IMAGE_NAME}:${env.GIT_COMMIT}"
        KUBECONFIG = credentials('kubeconfig-creds')
     }
    stages {
        stage('Setup') {
            steps {
                sh """
                python3 -m venv venv
                . venv/bin/activate
                pip install -r requirements.txt """
            }
        }

        /*stage('Test') {
            steps {
                sh "pytest"
            }
        }*/
        stage('Login to docker hub') {
            steps {
                withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')])
                    { sh 'echo ${PASSWORD} | docker login -u ${USERNAME} --password-stdin'}
                echo 'Login successfully'
            }
        }

        stage('Build Docker Image'){
            steps
            {
                sh 'docker build -t ${IMAGE_TAG} . '
                echo "Docker image build successfully"
                sh 'docker image ls'
            }
        }

        stage('Push Docker Image') {
            steps
            {
                sh 'docker push ${IMAGE_TAG}'
                echo "Docker image push successfully"
            }
        }

        stage('Deploy to Staging')
        {
            steps{
                sh 'kubectl config use-context staging-cluster'
                sh 'kubectl config current-context'
                sh 'kubectl set image deployment/flask-app flask-app=${IMAGE_TAG}'
            }
        }

        stage('Acceptance Test') {
            steps {
                script {
                     // start port-forwarding in the background
                     def portForward = sh(script: "kubectl port-forward service/flask-app-service 5000:5000 & echo \$!", returnStdout: true).trim()

                     // Wait to ensure port-forward is ready
                     sleep(time: 5, unit: 'SECONDS')

                     try {
                         sh "k6 run acceptance-test.js"
                     } finally {
                         // End the port forwarding process
                         sh "kill ${portForward}"
                     }
                 }
             }
         }

        stage('Deploy to prod') {
            steps {
                sh 'kubectl config use-context deployment-cluster'
                sh 'kubectl config current-context'
                sh 'kubectl set image deployment/flask-app flask-app=${IMAGE_TAG}'
            }
        }
    }
}