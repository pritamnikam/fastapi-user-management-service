"""Configuration management using Pydantic Settings.

Loads environment variables and provides application config.
"""
from dotenv import load_dotenv
from pydantic_settings import BaseSettings
import os

load_dotenv()

class Config(BaseSettings):
    """App configuration loaded from environment variables."""
    app_name: str = "PromptCatalog"
    debug: bool = False
    db_user: str = "admin"
    db_password: str = "secret"
    db_name: str = "prompt_catalog"
    db_host: str = "db"
    db_port: str = "5432"
    db_type: str = os.getenv("DB_TYPE", "postgresql")

    @property
    def db_url(self):
        """Constructs the database URL based on the selected type."""
        if self.db_type == "sqlite":
            return f"sqlite:///{self.db_name}"
        elif self.db_type == "postgresql":
            return (
                f"postgresql+psycopg2://{self.db_user}:{self.db_password}"
                f"@{self.db_host}:{self.db_port}/{self.db_name}"
            )
        else:
            raise ValueError(f"Invalid database type: {self.db_type}")


config = Config()