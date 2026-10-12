```groovy
pipeline {
    agent any

    stages {
        stage('Checkout') {
            steps {
                echo 'Source code checked out from GitHub'
            }
        }

        stage('Setup Python') {
            steps {
                bat '"C:\\Users\\BHARGAVI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" --version'

                bat '"C:\\Users\\BHARGAVI\\AppData\\Local\\Programs\\Python\\Python313\\python.exe" -m venv .venv-ci'

                bat '.venv-ci\\Scripts\\python.exe -m pip install --upgrade pip'

                bat '.venv-ci\\Scripts\\python.exe -m pip install -r requirements.txt'
            }
        }

        stage('Run Automated Tests') {
            steps {
                bat '.venv-ci\\Scripts\\python.exe -m pytest -v'
            }
        }
    }

    post {
        success {
            echo 'CI pipeline completed successfully!'
        }

        failure {
            echo 'CI pipeline failed. Check the console output.'
        }
    }
}
```