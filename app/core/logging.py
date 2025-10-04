"""Logging setup for the application."""

import logging

def setup_logging():
    """Configures logging format and level."""
    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s %(levelname)s [%(name)s] %(message)s"
    )