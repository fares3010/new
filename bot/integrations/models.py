from django.db import models
from django.utils import timezone
from django.core.validators import URLValidator
from create_agent.models import Agent

class Integration(models.Model):
    """
    Model representing an integration between an agent and an external service.
    
    Attributes:
        agent_id (ForeignKey): Reference to the associated Agent
        integration_id (IntegerField): Unique identifier for the integration
        integration_name (CharField): Name of the integration
        integration_type (CharField): Type of integration (e.g., 'api', 'webhook', 'oauth')
        integration_url (URLField): URL endpoint for the integration
        integration_key (CharField): API key or access key
        integration_secret (CharField): Secret key for authentication
        integration_token (CharField): Access token for OAuth integrations
        description (TextField): Detailed description of the integration
        created_at (DateTimeField): Timestamp of creation
        updated_at (DateTimeField): Timestamp of last update
        is_active (BooleanField): Whether the integration is active
        is_deleted (BooleanField): Soft delete flag
        is_archived (BooleanField): Archive flag
        configuration (JSONField): Additional configuration settings
        meta_data (JSONField): Additional metadata
    """
    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        related_name='integrations',
        help_text="The agent this integration belongs to"
    )
    integration_id = models.AutoField(primary_key=True)  # Changed to AutoField for auto-incrementing
    integration_name = models.CharField(
        max_length=255,
        help_text="Name of the integration"
    )
    integration_type = models.CharField(
        max_length=50,
        help_text="Type of integration (e.g., 'api', 'webhook', 'oauth')"
    )
    integration_url = models.URLField(
        max_length=200, 
        blank=True, 
        null=True,
        validators=[URLValidator()],
        help_text="URL endpoint for the integration"
    )
    integration_key = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="API key or access key"
    )
    integration_secret = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Secret key for authentication"
    )
    integration_token = models.CharField(
        max_length=255, 
        blank=True, 
        null=True,
        help_text="Access token for OAuth integrations"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the integration"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp of creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last update"
    )
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the integration is active"
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag"
    )
    is_archived = models.BooleanField(
        default=False,
        help_text="Archive flag"
    )
    configuration = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Additional configuration settings"
    )
    meta_data = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Additional metadata"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Integration'
        verbose_name_plural = 'Integrations'
        indexes = [
            models.Index(fields=['integration_type']),
            models.Index(fields=['is_active']),
            models.Index(fields=['created_at']),
        ]

    def __str__(self):
        return f"{self.integration_name} ({self.integration_type})"
    
    def get_integration_details(self):
        """
        Returns a dictionary of integration details.
        
        Returns:
            dict: A dictionary containing all integration details
        """
        return {
            "integration_id": self.integration_id,
            "integration_name": self.integration_name,
            "integration_type": self.integration_type,
            "integration_url": self.integration_url,
            "integration_key": self.integration_key,
            "integration_secret": self.integration_secret,
            "integration_token": self.integration_token,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
            "is_archived": self.is_archived,
            "configuration": self.configuration,
            "meta_data": self.meta_data,
            "agent": self.agent.id,  # Added agent_id to the details
        }

    def to_dict(self):
        """
        Alias for get_integration_details for backward compatibility.
        
        Returns:
            dict: A dictionary containing all integration details
        """
        return self.get_integration_details()
    
class IntegrationCategory(models.Model):
    """
    Model representing a category of integrations.
    
    Attributes:
        category_id (IntegerField): Unique identifier for the category
        category_name (CharField): Name of the category
        description (TextField): Detailed description of the category
        created_at (DateTimeField): Timestamp of creation
        updated_at (DateTimeField): Timestamp of last update
        is_active (BooleanField): Whether the category is active
        is_deleted (BooleanField): Soft delete flag
    """
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(
        max_length=255,
        help_text="Name of the category"
    )
    agent = models.ForeignKey(
        Agent, 
        on_delete=models.CASCADE, 
        related_name='integration_categories',
        help_text="The agent this integration category belongs to"
    )
    description = models.TextField(
        blank=True,
        help_text="Detailed description of the category"
    )
    created_at = models.DateTimeField(
        default=timezone.now,
        help_text="Timestamp of creation"
    )
    updated_at = models.DateTimeField(
        auto_now=True,
        help_text="Timestamp of last update"
    )   
    is_active = models.BooleanField(
        default=True,
        help_text="Whether the category is active"
    )
    is_deleted = models.BooleanField(
        default=False,
        help_text="Soft delete flag"
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = 'Integration Category'
        verbose_name_plural = 'Integration Categories'  

    def __str__(self):
        return self.category_name

    def get_category_details(self):
        return {
            "category_id": self.category_id,
            "category_name": self.category_name,
            "description": self.description,
            "created_at": self.created_at,
            "updated_at": self.updated_at,
            "is_active": self.is_active,
            "is_deleted": self.is_deleted,
        }

    def to_dict(self):
        return self.get_category_details()                                                      