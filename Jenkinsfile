pipeline {
    agent any

    environment {
        DATABASE_URL = 'postgresql+psycopg://test_user:test_password@postgres-test:5432/test_db'
        TEST_DATABASE_URL = 'postgresql+psycopg://test_user:test_password@postgres-test:5432/test_db'
        REDIS_URL = 'redis://redis:6379/0'
        JWT_SECRET_KEY = 'jenkins-test-secret-not-for-production'
        JWT_ALGORITHM = 'HS256'
        ACCESS_TOKEN_EXPIRE_MINUTES = '30'

        REGISTRY = 'ghcr.io'
        IMAGE_NAME = 'ghcr.io/caribbeancool/backend-platform'
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
                script {
                    env.IMAGE_TAG = sh(
                        script: 'git rev-parse --short HEAD',
                        returnStdout: true
                    ).trim()
                }

                sh '''
                    docker build \
                    --target production \
                    --label org.opencontainers.image.source=https://github.com/CaribbeanCool/backend-platform \
                    --label org.opencontainers.image.revision=$GIT_COMMIT \
                    -t $IMAGE_NAME:$IMAGE_TAG .
                '''
            }
        }
        stage('Push Image') {
            steps {
                withCredentials([
                    usernamePassword(
                        credentialsId: 'ghcr-credentials',
                        usernameVariable: 'GHCR_USERNAME',
                        passwordVariable: 'GHCR_TOKEN'
                    )
                ]) {
                    sh '''
                        echo "$GHCR_TOKEN" | docker login $REGISTRY \
                        -u "$GHCR_USERNAME" \
                        --password-stdin

                        docker push $IMAGE_NAME:$IMAGE_TAG
                    '''
                }
    }
}
    }

    post {
        always {
            sh 'docker logout ghcr.io || true'
            echo 'Pipeline finished.'
        }

        success {
            echo 'All CI quality gates passed and the image was published.'
        }

        failure {
            echo 'At least one pipeline stage failed.'
        }
    }
}