"""
Bot project initialization.

This module initializes the Django application and sets up any necessary
configuration for the bot project.
"""

import os
from pathlib import Path

# Add project root to Python path
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in os.sys.path:
    os.sys.path.append(str(project_root))

# Set default Django settings module
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'bot.settings')

# Initialize Django
import django
django.setup()

# Optional: Add any project-wide initialization here
try:
    from django.conf import settings
    if not settings.configured:
        raise RuntimeError("Django settings not properly configured")
except ImportError as e:
    raise RuntimeError(f"Failed to import Django settings: {e}")
                                                                    