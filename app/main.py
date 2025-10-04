"""Main entrypoint for FastAPI application.

- Initializes logging and database schema.
- Creates FastAPI app instance.
- Registers API routes.
"""

from fastapi import FastAPI

from app.api.v1 import user, prompt, admin
from app.core.config import config
from app.core.logging import setup_logging
from app.db.schema import Base, engine

setup_logging()
Base.metadata.create_all(bind=engine)

app = FastAPI(title=config.app_name)

# Register API routes
app.include_router(user.router, prefix="/api/v1")
app.include_router(prompt.router, prefix="/api/v1")
app.include_router(admin.router)