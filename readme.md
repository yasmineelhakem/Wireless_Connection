# Wi-Fi Monitoring Flask Application

 `Flask`, `Wi-Fi Monitoring`, `Real-Time`, `Docker`, `Kubernetes`, `CI/CD`, `Jenkins`, `k6`

This project is a Flask-based web application designed to monitor available Wi-Fi networks, display their signal strengths, and connect to the strongest network. It includes a real-time frontend powered by Flask-SocketIO and a Jenkins pipeline for automated CI/CD.

---

## Features

- **Real-Time Frontend**: Displays Wi-Fi networks and their signal strengths dynamically.
- **Backend Automation**: Fetches Wi-Fi details and connects to the strongest network.
- **Dockerized**: Fully containerized for consistent deployment.
- **Kubernetes Deployment**: Supports staging and production environments.
- **Automated CI/CD**: Jenkins pipeline for building, testing, and deploying the application.
- **Acceptance Testing**: Uses `k6` for performance and functionality validation.

---

## CI/CD Pipeline

The Jenkins pipeline automates the build, test, and deployment process. Below is an overview of the pipeline stages:

### Pipeline Stages

1. **Setup**:
    - Creates a Python virtual environment.
    - Installs dependencies from `requirements.txt`.

2. **Login to Docker Hub**:
    - Authenticates with Docker Hub using Jenkins credentials.

3. **Build Docker Image**:
    - Builds a Docker image for the application.
    - Tags the image with the Git commit hash for versioning.

4. **Push Docker Image**:
    - Pushes the Docker image to Docker Hub.
    - [Docker Hub Repository](https://hub.docker.com/repository/docker/yasmine650/jenkins-flask-app/general)

5. **Deploy to Staging**:
    - Switches Kubernetes context to the staging cluster.
    - Updates the deployment with the new Docker image.

6. **Acceptance Test**:
    - Sets up port forwarding to expose the application.
    - Runs `k6` acceptance tests to validate functionality and performance.
    - Cleans up port-forwarding processes after tests.

7. **Deploy to Production**:
    - Switches Kubernetes context to the production cluster.
    - Updates the deployment with the new Docker image.

---

## Kubernetes Deployment

The application is deployed to Kubernetes using the following configuration files:

- **`deployment.yaml`**: Defines the deployment with 3 replicas.
- **`service.yaml`**: Exposes the application on port 5000.
