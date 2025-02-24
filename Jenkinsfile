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
                bat """
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
               withCredentials([usernamePassword(credentialsId: 'docker-cred', usernameVariable: 'USERNAME', passwordVariable: 'PASSWORD')]) {
                   bat 'echo | set /p="%PASSWORD%" | docker login -u %USERNAME% --password-stdin'
               }
               echo 'Login successfully'
           }
       }

        stage('Build Docker Image') {
            steps {
                bat 'docker build -t %IMAGE_TAG% .'
                echo "Docker image build successfully"
                bat 'docker image ls'
            }
        }

        stage('Push Docker Image') {
            steps {
                bat 'docker push %IMAGE_TAG%'
                echo "Docker image push successfully"
            }
        }

        stage('Deploy to Staging')
        {
            steps{
                bat 'kubectl config use-context staging-cluster'
                bat 'kubectl config current-context'
                bat 'kubectl set image deployment/flask-app flask-app=${IMAGE_TAG}'
            }
        }

         stage('Acceptance Test') {
             steps {
                 script {
                     def portForwardScript = """
                         @echo off
                         kubectl port-forward service/flask-app-service 5000:5000
                     """
                     writeFile file: 'port-forward.bat', text: portForwardScript
                     bat 'start /B port-forward.bat'
                     sleep(time: 5, unit: 'SECONDS')

                     try {
                         // Run the acceptance tests
                         bat "k6 run acceptance-test.js"
                     } finally {
                         // End the port forwarding process
                         bat "taskkill /F /IM kubectl.exe"
                     }
                 }
             }
         }

        stage('Deploy to prod') {
            steps {
                bat 'kubectl config use-context deployment-cluster'
                bat 'kubectl config current-context'
                bat 'kubectl set image deployment/flask-app flask-app=${IMAGE_TAG}'
            }
        }
    }
}