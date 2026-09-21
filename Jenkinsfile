pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgresql+psycopg://test_user:test_password@postgres-test:5432/test_db'
        TEST_DATABASE_URL = 'postgresql+psycopg://test_user:test_password@postgres-test:5432/test_db'
        REDIS_URL = 'redis://redis:6379/0'
        JWT_SECRET_KEY = 'jenkins-test-secret-not-for-production'
        JWT_ALGORITHM = 'HS256'
        ACCESS_TOKEN_EXPIRE_MINUTES = '30'
    }

    stages {
        stage('Setup') {
            steps {
                sh '''
                    python3 -m venv .venv
                    .venv/bin/pip install --upgrade pip
                    .venv/bin/pip install -r requirements-dev.txt
                    .venv/bin/pip check
                '''
            }
        }

        stage('Lint') {
            steps {
                sh '.venv/bin/ruff check .'
            }
        }

        stage('Migrations') {
    steps {
        sh '.venv/bin/alembic upgrade head'
    }
}

        stage('Test') {
            steps {
                sh '.venv/bin/pytest -v --cov=app --cov-report=term-missing'
            }
        }

        stage('Production Image') {
            steps {
                sh '''
                    docker build \
                      --target production \
                      -t backend-platform:jenkins .
                '''
            }
        }
    }

    post {
        always {
            echo 'Pipeline finished.'
        }

        success {
            echo 'All CI quality gates passed.'
        }

        failure {
            echo 'At least one CI quality gate failed.'
        }
    }
}