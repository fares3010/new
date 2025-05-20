"""
ASGI config for bot project.

It exposes the ASGI callable as a module-level variable named ``application``.

For more information on this file, see
https://docs.djangoproject.com/en/5.2/howto/deployment/asgi/
"""

import os
import sys
from pathlib import Path

# Add the project root directory to Python path
project_root = Path(__file__).resolve().parent.parent
sys.path.append(str(project_root))

from django.core.asgi import get_asgi_application

# Set Django settings module
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "bot.settings")

# Initialize ASGI application
application = get_asgi_application()

# Optional: Add error handling for production
try:
    # Verify settings module is properly configured
    from django.conf import settings
    if not settings.configured:
        raise RuntimeError("Django settings not properly configured")
except ImportError as e:
    raise RuntimeError(f"Failed to import Django settings: {e}")
