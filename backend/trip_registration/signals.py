"""
Trip Registration Signals
Handle post-save/post-delete signals for registration events
"""
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.core.mail import send_mail
from django.conf import settings
import logging

from .models import PilgrimageClient, PilgrimageClientTmp

logger = logging.getLogger(__name__)


@receiver(post_save, sender=PilgrimageClient)
def registration_confirmed(sender, instance, created, **kwargs):
    """
    Send confirmation email when a registration is confirmed
    """
    if created:
        try:
            # Send confirmation email to the lead passenger
            # This would be implemented based on your email template structure
            logger.info(f"Registration confirmed for pilgrimage {instance.pilgrimage_id}, client {instance.client_id}")
            
            # TODO: Implement email sending
            # send_confirmation_email(instance)
            
        except Exception as e:
            logger.error(f"Error sending confirmation email: {str(e)}")


@receiver(post_delete, sender=PilgrimageClientTmp)
def temp_registration_cleanup(sender, instance, **kwargs):
    """
    Log when temporary registrations are cleaned up
    """
    logger.info(f"Temporary registration {instance.id} cleaned up (session: {instance.session_id})")


def send_confirmation_email(registration):
    """
    Send registration confirmation email
    This would be implemented based on your email template structure
    """
    # TODO: Implement email template and sending logic
    pass
