"""Configuration management using Pydantic Settings.

Loads environment variables and provides application config.
"""

from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class Config(BaseSettings):
    """App configuration loaded from environment variables."""
    app_name: str = "ScalableFastAPIProject"
    debug: bool = False
    db_user: str = ""
    db_password: str = ""
    db_name: str = "test.db"

    @property
    def db_url(self):
        """Constructs the database URL for SQLite."""
        return f"sqlite:///./{self.db_name}"


config = Config()