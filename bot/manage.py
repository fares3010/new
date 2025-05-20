#!/usr/bin/env python
"""Django's command-line utility for administrative tasks."""
import os
import sys
import logging
from pathlib import Path

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def check_environment():
    """Verify the Python environment and Django installation."""
    try:
        import django
        logger.info(f"Django version: {django.get_version()}")
        return True
    except ImportError:
        logger.error("Django is not installed")
        return False

def main():
    """Run administrative tasks with enhanced error handling and logging."""
    try:
        # Set Django settings module
        settings_module = "bot.settings"
        os.environ.setdefault("DJANGO_SETTINGS_MODULE", settings_module)
        logger.info(f"Using settings module: {settings_module}")

        # Verify Django installation
        if not check_environment():
            raise ImportError("Django installation check failed")

        # Import and execute Django management commands
        from django.core.management import execute_from_command_line
        logger.debug(f"Executing command: {' '.join(sys.argv)}")
        execute_from_command_line(sys.argv)

    except ImportError as exc:
        logger.error("Django import error", exc_info=True)
        raise ImportError(
            "Couldn't import Django. Are you sure it's installed and "
            "available on your PYTHONPATH environment variable? Did you "
            "forget to activate a virtual environment?"
        ) from exc
    except Exception as e:
        logger.error(f"Unexpected error: {str(e)}", exc_info=True)
        raise

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        logger.critical(f"Fatal error: {str(e)}", exc_info=True)
        sys.exit(1)
