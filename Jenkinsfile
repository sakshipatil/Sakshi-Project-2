pipeline {
    agent any
    stages {
        stage('Build') {
            steps {
                echo "python build"
                sh 'python --version'

                sh 'pip3 install -r requirements.txt'
                echo 'Building..'
            }
        }
        stage('Test') {
            steps {
                echo "python test"
                sh 'python3 test.py'
            }
        }
        stage('Deploy') {
            steps {
               echo "python deploy"
               sh 'python3 app.py &'
            }
        }
    }
}
