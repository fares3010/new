from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Conversation, Message

@receiver(post_save, sender=Conversation)
def handle_conversation_created(sender, instance, created, **kwargs):
    """Signal handler for when a conversation is created"""
    if created:
        # Add any post-creation actions here
        pass

@receiver(post_save, sender=Message)
def handle_message_created(sender, instance, created, **kwargs):
    """Signal handler for when a message is created"""
    if created:
        # Add any post-creation actions here
        pass 