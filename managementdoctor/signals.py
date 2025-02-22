from django.db.models.signals import post_delete
from django.dispatch import receiver
from .models import Doctor

@receiver(post_delete, sender=Doctor)
def delete_associated_credential(sender, instance, **kwargs):
    # Delete credential associated to the Doctor
    if instance.credential:
        instance.credential.delete()