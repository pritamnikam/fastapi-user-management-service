# AI Prompt Catalog Backend

A production-ready FastAPI backend for managing and externalizing LLM prompts, designed for integration with AI applications.  
Features a PostgreSQL database, REST API, and an admin portal for prompt management.

## Features

- **Prompt Catalog:** CRUD API for storing and managing AI prompts
- **User Management:** Example user CRUD endpoints
- **Admin Portal:** Web interface for prompt administration
- **PostgreSQL Database:** Reliable, scalable storage
- **Containerized:** Docker & Compose for easy deployment
- **Best Practices:** Modern Python, type hints, modular structure

## Getting Started

### Prerequisites

- Python 3.13+
- Docker & Docker Compose

### Local Development

1. Install dependencies:
    ```sh
    uv sync
    ```
2. Start the server:
    ```sh
    uv run uvicorn app.main:app --reload
    ```

### Docker Deployment

1. Build and run with Docker Compose:
    ```sh
    docker compose up --build
    ```
2. The API will be available at [http://localhost:8000/api/v1/prompts](http://localhost:8000/api/v1/prompts)
3. The admin portal is at [http://localhost:8000/admin](http://localhost:8000/admin)

### API Usage Examples

#### Create a Prompt
```sh
curl -X POST "http://localhost:8000/api/v1/prompts" \
     -H "Content-Type: application/json" \
     -d '{"name": "Summarize", "content": "Summarize the following text:", "description": "General summary prompt"}'
```

#### List Prompts
```sh
curl -X GET "http://localhost:8000/api/v1/prompts"
```

#### Update a Prompt
```sh
curl -X PUT "http://localhost:8000/api/v1/prompts/1" \
     -H "Content-Type: application/json" \
     -d '{"name": "Summarize", "content": "Summarize this:", "description": "Updated prompt"}'
```

#### Delete a Prompt
```sh
curl -X DELETE "http://localhost:8000/api/v1/prompts/1"
```

## Environment Variables

See `.env.example` for required variables (used by Docker Compose).

## Project Structure

```
project/
  app/
    api/v1/         # API routes (user, prompt, admin)
    core/           # Config and logging
    db/             # Database schema
    models/         # Pydantic models
    services/       # Business logic
    main.py         # FastAPI app entrypoint
  tests/            # Pytest tests
  Dockerfile
  docker-compose.yaml
  .env.example
  pyproject.toml
  .gitignore
  .dockerignore
```