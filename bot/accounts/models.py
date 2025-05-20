from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone


class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    Uses email as the unique identifier instead of username.
    """
    # Remove username field since we'll use email as the identifier
    username = None
    
    # Make email the unique identifier
    email = models.EmailField(_('email address'), unique=True)
    
    # Add full name field
    full_name = models.CharField(_('full name'), max_length=255, blank=True)
    
    # Add profile image field
    profile_image = models.ImageField(
        _('profile image'),
        upload_to='profile_images/',
        null=True,
        blank=True
    )
    
    # Add last profile update timestamp
    profile_updated_at = models.DateTimeField(
        _('profile updated at'),
        default=timezone.now
    )
    
    # Use email as the username field
    USERNAME_FIELD = 'email'
    
    # Required fields for createsuperuser
    REQUIRED_FIELDS = ['full_name']
    
    class Meta:
        verbose_name = _('user')
        verbose_name_plural = _('users')
        ordering = ['-date_joined']
        
    def __str__(self):
        return self.email
    
    def get_full_name(self):
        """
        Get the full name of the user.
        Returns the full_name field if set, otherwise falls back to parent method.
        """
        return self.full_name or super().get_full_name()
    
    def get_short_name(self):
        """
        Get the short name of the user.
        Returns the first name if set, otherwise returns the email username.
        """
        return self.first_name or self.email.split('@')[0]
    
    def email_user(self, subject, message, from_email=None, **kwargs):
        """
        Send an email to the user.
        Uses Django's send_mail function with proper error handling.
        """
        if not from_email:
            from_email = settings.DEFAULT_FROM_EMAIL
        try:
            send_mail(subject, message, from_email, [self.email], **kwargs)
        except Exception as e:
            # Log the error but don't raise it to prevent application crashes
            print(f"Failed to send email to {self.email}: {str(e)}")
    
    def get_profile_image_url(self):
        """
        Get the profile image URL of the user.
        Returns the URL of the profile image if it exists, otherwise returns a default image URL.
        """
        if self.profile_image and hasattr(self.profile_image, 'url'):
            return self.profile_image.url
        return f'{settings.STATIC_URL}images/default_profile.png'
    
    def update_profile_image(self, image_file):
        """
        Update the user's profile image.
        Updates the profile_image field and sets the profile_updated_at timestamp.
        """
        self.profile_image = image_file
        self.profile_updated_at = timezone.now()
        self.save(update_fields=['profile_image', 'profile_updated_at'])
