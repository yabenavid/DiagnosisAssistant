from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Doctor
from django.contrib.auth.models import User

@receiver(post_delete, sender=Doctor)
def delete_associated_user(sender, instance, **kwargs):
    # Delete user associated to the Doctor
    if instance.user:
        instance.user.delete()