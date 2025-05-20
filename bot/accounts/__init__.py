
"""
Initialization module for the accounts app.

This module handles the initialization of the accounts app, including:
- Signal registrations for user-related events
- Custom user model configuration
- Authentication-related setup
"""

from django.apps import AppConfig


class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'User Accounts'

    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        This includes registering signals and other app-specific setup.
        """
        try:
            import accounts.signals  # noqa
        except ImportError:
            pass  # Signals module may not exist yet
