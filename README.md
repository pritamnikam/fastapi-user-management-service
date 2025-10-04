# Scalable FastAPI User Management Service

A robust FastAPI REST API for user management, featuring SQLAlchemy ORM, Pydantic models, Docker support, and comprehensive testing.

## Features

- FastAPI RESTful endpoints for CRUD operations on users
- SQLAlchemy ORM for database interactions
- Pydantic models for request/response validation
- Docker and Compose for containerized deployment
- Environment variable support via `.env`
- Pytest-based unit and integration tests

## Getting Started

### Prerequisites

- Python 3.13+
- Docker (optional for containerized deployment)
- [uv](https://github.com/astral-sh/uv) for dependency management

### Installation (Local)

```sh
uv sync
```

### Running the Server Locally

```sh
uv run uvicorn app.main:app --reload
```

Server runs at [http://localhost:8000](http://localhost:8000).

## Docker Usage

### Build the Docker Image

```sh
docker build -t fastapi-user-service .
```

### Run the Container

```sh
docker run -d -p 8000:8000 --env-file .env fastapi-user-service
```

### Using Docker Compose

```sh
docker compose up --build
```

## Dockerfile Overview

The `Dockerfile` typically:

- Uses an official Python base image
- Installs dependencies from `requirements.txt` or `pyproject.toml`
- Copies application code into the container
- Sets environment variables
- Runs the FastAPI app with Uvicorn

Example snippet:

```dockerfile
FROM python:3.13-slim

WORKDIR /app

COPY pyproject.toml ./
RUN pip install --upgrade pip && pip install uv

COPY . .

EXPOSE 8000

CMD ["uv", "run", "uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

## API Usage Examples

#### Create a User

```sh
curl -X POST "http://localhost:8000/api/v1/users" \
     -H "Content-Type: application/json" \
     -d '{"name": "Ada Lovelace"}'
```

#### Get All Users

```sh
curl -X GET "http://localhost:8000/api/v1/users"
```

#### Get a User by ID

```sh
curl -X GET "http://localhost:8000/api/v1/users/1"
```

#### Update a User

```sh
curl -X PUT "http://localhost:8000/api/v1/users/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Grace Hopper"}'
```

#### Delete a User

```sh
curl -X DELETE "http://localhost:8000/api/v1/users/1"
```

## Testing

```sh
pytest
```

## Environment Variables

See `.env.example` for required variables.

## Project Structure

```
project/
  app/
    api/v1/         # API routes
    core/           # Config and logging
    db/             # Database schema
    models/         # Pydantic models
    services/       # Business logic
    main.py         # FastAPI app entrypoint
  tests/            # Pytest tests
  Dockerfile
  docker-compose.yaml
  .env.example
  .python-version
  test.db
```

---