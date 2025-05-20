from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth import get_user_model
from django.core.exceptions import ValidationError
import logging

logger = logging.getLogger(__name__)
User = get_user_model()

@receiver(post_save, sender=User, dispatch_uid='create_user_profile')
def create_user_profile(sender, instance, created, **kwargs):
    """
    Signal handler to perform actions after a user is created.
    
    Args:
        sender: The model class that sent the signal
        instance: The actual instance being saved
        created: Boolean indicating if this is a new instance
        **kwargs: Additional keyword arguments
    """
    try:
        if created:
            # Log the user creation with sender model name
            logger.info(f"New user created via {sender.__name__}: {instance.email}")
            
            # Validate user data
            if not instance.email:
                raise ValidationError("Email is required")
            
            # Add any additional post-creation actions here
            # For example:
            # - Create associated profile
            # - Send welcome email
            # - Set up initial preferences
            
            logger.debug(f"User profile setup completed for: {instance.email}")
            
    except Exception as e:
        logger.error(f"Error in create_user_profile signal for {sender.__name__}: {str(e)}")
        # Re-raise the exception to ensure proper error handling
        raise