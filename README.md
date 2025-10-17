# AI Prompt Catalog Backend

A production-ready FastAPI backend for managing and externalizing LLM prompts, designed for integration with AI applications.  
Features a PostgreSQL database, REST API, and an admin portal for prompt management with versioning support.

## Features

- **Prompt Catalog:** CRUD API for storing and managing AI prompts with versioning
- **Multi-Application Support:** Organize prompts by application ID
- **Version Control:** Track prompt history with automatic versioning
- **User Management:** Example user CRUD endpoints
- **Admin Portal:** Interactive web interface for prompt administration
- **PostgreSQL Database:** Reliable, scalable storage with data integrity
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
3. Start streamlit app
   ```sh
   uv run streamlit run app/streamlit_app.py --server.port 8501 --server.address 0.0.0.0
   ```

### Docker Deployment

1. Build and run with Docker Compose:
    ```sh
    docker compose up --build
    ```
2. The FastAPI backend will be available at [http://localhost:8000/api/v1/prompts](http://localhost:8000/api/v1/prompts)
3. The Streamlit Admin Portal will be available at [http://localhost:8501](http://localhost:8501)

### Admin Portal

The Streamlit Admin Portal provides a comprehensive interface for managing prompts with the following features:

- **Application Selector:** Choose the target application from a dynamically populated dropdown
- **Prompt List:** View all prompts for the selected application with version information
- **Prompt Editor:** Create and edit prompt content with automatic versioning
- **History & Rollback:** View complete version history with the ability to restore previous versions
- **Multi-User Support:** Track changes by user with the created_by field

The portal is designed for ease of use while providing powerful prompt management capabilities:

- **Version Management:** Each edit creates a new version while preserving history
- **Active Version Control:** Only one version of each prompt is active at a time
- **Intuitive Interface:** Clear organization with tabular displays of prompts and versions
- **Real-time Feedback:** Immediate confirmation of successful operations

### Prompt Schema

The prompt system uses a robust schema designed for versioning and multi-application support:

- **app_id:** Application identifier for organizing prompts
- **prompt_key:** Unique identifier for the prompt within an application
- **prompt_text:** The actual prompt content
- **version:** Automatically incremented version number
- **is_active:** Flag indicating the currently active version
- **created_by:** User who created this version
- **created_at:** Timestamp of creation

### API Usage Examples

#### Create a Prompt
```sh
curl -X POST "http://localhost:8000/api/v1/prompts" \
     -H "Content-Type: application/json" \
     -d '{
       "app_id": "chatbot",
       "prompt_key": "greeting",
       "prompt_text": "You are a friendly assistant. Greet the user warmly.",
       "created_by": "admin",
       "is_active": true
     }'
```

#### List All Prompts
```sh
curl -X GET "http://localhost:8000/api/v1/prompts"
```

#### List Prompts for a Specific Application
```sh
curl -X GET "http://localhost:8000/api/v1/prompts?app_id=chatbot"
```

#### Get Active Prompt Version
```sh
curl -X GET "http://localhost:8000/api/v1/prompts/active/chatbot/greeting"
```

#### Update a Prompt (Creates New Version)
```sh
curl -X PUT "http://localhost:8000/api/v1/prompts/1" \
     -H "Content-Type: application/json" \
     -d '{
       "prompt_text": "You are a friendly and helpful assistant. Greet the user warmly.",
       "is_active": true
     }'
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
    streamlit_app.py # Streamlit admin portal
  tests/            # Pytest tests
  Dockerfile
  docker-compose.yaml
  .env.example
  pyproject.toml
  .gitignore
  .dockerignore
```