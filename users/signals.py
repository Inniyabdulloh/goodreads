from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.mail import send_mail
from .models import CustomUser
@receiver(post_save, sender=CustomUser)
def send_welcome_email(sender, instance, created, **kwargs):
    if created:
        if instance.email:
            send_mail(
                subject="New Goodreads User",
                message='Thank you for registering for Goodreads.',
                from_email=settings.EMAIL_HOST_USER,
                recipient_list=[instance.email],
        )

