# Backend Platform

Backend Platform is a FastAPI service for user authentication and product
management. It uses PostgreSQL for persistence, Redis for caching, Alembic for
database migrations, and Prometheus-compatible metrics.

## Requirements

Choose either the Docker workflow or the local Python workflow:

- Docker Engine 24+ and Docker Compose v2 (recommended)
- Or Python 3.13+, PostgreSQL 17, and Redis 7

## Configuration

The application reads configuration from environment variables and, when
running locally, from a `.env` file in the project root.

Create a local environment file:

```bash
cp .env.example .env
```

For a host-Python installation, use hostnames and ports reachable from your
machine:

```dotenv
DATABASE_URL=postgresql+psycopg://backend_user:backend_password@localhost:5432/backend_db
REDIS_URL=redis://localhost:6379/0
CACHE_TTL_SECONDS=60
JWT_SECRET_KEY=replace-with-a-long-random-secret
JWT_ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

The Docker Compose workflow uses the service names `postgres` and `redis`
instead of `localhost`:

```dotenv
DATABASE_URL=postgresql+psycopg://backend_user:backend_password@postgres:5432/backend_db
REDIS_URL=redis://redis:6379/0
```

Use a unique, securely generated `JWT_SECRET_KEY` outside local development.
Do not commit `.env` or production credentials.

## Run with Docker Compose

Start the application and its supporting services:

```bash
docker compose up --build -d
```

Apply the database migrations once the services are healthy:

```bash
docker compose exec api alembic upgrade head
```

The API is available directly at <http://localhost:8000>. The Compose stack
also includes Kong as a gateway, so the same API routes are available through
<http://localhost:8000> after Kong starts. The development container reloads
when source files change.

To follow application logs:

```bash
docker compose logs -f api
```

To stop the stack:

```bash
docker compose down
```

To stop the stack and remove its persistent PostgreSQL, Grafana, and Jenkins
data volumes:

```bash
docker compose down -v
```

### Compose services

| Service | Purpose | Address |
| --- | --- | --- |
| `api` | FastAPI development server | `http://localhost:8000` |
| `postgres` | Application database | `localhost:5432` |
| `redis` | Cache | `localhost:6379` |
| `prometheus` | Metrics collection | `http://localhost:9090` |
| `grafana` | Dashboards | `http://localhost:3000` |
| `jenkins` | CI server | `http://localhost:8080` |

The `postgres-test` service is intended for containerized test runs. It is not
published to a host port by default.

## Run locally with Python

Start PostgreSQL and Redis, for example by running only those Compose services:

```bash
docker compose up -d postgres redis
```

Create a virtual environment and install development dependencies:

```bash
python3.13 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
python -m pip install -r requirements-dev.txt
```

Set the environment variables from the host configuration above, then apply
migrations:

```bash
alembic upgrade head
```

Start the development server:

```bash
uvicorn app.main:app --reload
```

The server listens on <http://127.0.0.1:8000> by default.

## API usage

Interactive API documentation is available at:

- Swagger UI: <http://localhost:8000/docs>
- ReDoc: <http://localhost:8000/redoc>
- Prometheus metrics: <http://localhost:8000/metrics>
- Health check: <http://localhost:8000/health>

The main API routes are:

| Method | Route | Authentication |
| --- | --- | --- |
| `POST` | `/api/v1/auth/register` | Public |
| `POST` | `/api/v1/auth/login` | Public |
| `GET` | `/api/v1/products` | Public |
| `GET` | `/api/v1/products/{product_id}` | Public |
| `POST` | `/api/v1/products` | Bearer token |
| `PATCH` | `/api/v1/products/{product_id}` | Public |
| `DELETE` | `/api/v1/products/{product_id}` | Public |

Register and log in to receive a token:

```bash
curl -X POST http://localhost:8000/api/v1/auth/register \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"change-me"}'

curl -X POST http://localhost:8000/api/v1/auth/login \
  -H 'Content-Type: application/json' \
  -d '{"email":"user@example.com","password":"change-me"}'
```

Use the returned `access_token` for protected requests:

```bash
curl -X POST http://localhost:8000/api/v1/products \
  -H "Authorization: Bearer <access-token>" \
  -H 'Content-Type: application/json' \
  -d '{"name":"Example product","description":"An example"}'
```

## Database migrations

Create a migration after changing the SQLAlchemy models:

```bash
alembic revision --autogenerate -m "describe the schema change"
```

Apply or roll back migrations:

```bash
alembic upgrade head
alembic downgrade -1
```

## Tests and linting

The test suite requires PostgreSQL and Redis. Start the application database
and export a test database URL when running tests from the host:

```bash
docker compose up -d postgres redis
export DATABASE_URL=postgresql+psycopg://backend_user:backend_password@localhost:5432/backend_db
export TEST_DATABASE_URL=postgresql+psycopg://backend_user:backend_password@localhost:5432/backend_db
export REDIS_URL=redis://localhost:6379/0
export JWT_SECRET_KEY=local-test-secret
```

Run the checks:

```bash
pytest -v --cov=app --cov-report=term-missing
ruff check .
pip check
```

## Production image

Build the non-reloading production image:

```bash
docker build --target production -t backend-platform:latest .
```

Run it with the required configuration and a reachable PostgreSQL and Redis
instance:

```bash
docker run --rm -p 8000:8000 \
  --env-file .env \
  backend-platform:latest
```

Run migrations against the same database before serving traffic:

```bash
docker run --rm --env-file .env \
  backend-platform:latest \
  alembic upgrade head
```

The production image runs as the non-root `appuser` user and listens on port
8000.

## Project layout

```text
app/                 FastAPI application, routes, services, and repositories
alembic/             Database migration configuration and revisions
gateway/             Kong declarative gateway configuration
monitoring/          Prometheus scrape and alert configuration
tests/               Unit and integration tests
Dockerfile           Development and production image stages
docker-compose.yml   Local development and supporting services
```
