from django.apps import AppConfig
from django.conf import settings
import logging

logger = logging.getLogger(__name__)

class AccountsConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'accounts'
    verbose_name = 'User Accounts'

    def ready(self):
        """
        Initialize the accounts app and connect signals.
        This method is called when Django starts.
        """
        if settings.DEBUG:
            logger.debug("Initializing accounts app...")
        
        try:
            from . import signals  # This will automatically connect the signals via @receiver
            if settings.DEBUG:
                logger.debug("User profile signals initialized successfully")
        except Exception as e:
            logger.error(f"Error initializing signals: {str(e)}")
            raise
