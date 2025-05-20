# This file can be used to define package-level initialization code for the 'conversations' app.
# For now, no initialization is required. You can add signal registrations or other setup here if needed in the future.
"""
Initialization module for the conversations app.

This module handles the initialization of the conversations app, including:
- Signal registrations for conversation-related events
- Message handling setup
- Conversation management configuration
"""

from django.apps import AppConfig


class ConversationsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'conversations'
    verbose_name = 'Conversations'

    def ready(self):
        """
        Perform initialization tasks when the app is ready.
        This includes registering signals and other app-specific setup.
        """
        try:
            import conversations.signals  # noqa
        except ImportError:
            pass  # Signals module may not exist yet
