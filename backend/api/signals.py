from django.db.models.signals import post_save
from django.dispatch import receiver
from django.utils import timezone
from .models import EscrowTransaction, User, Profile



@receiver(post_save, sender=EscrowTransaction)
def auto_release_escrow(sender, instance, **kwargs):
    if not instance.released and timezone.now() >= instance.release_date:
        instance.status = 'released'
        instance.released = True
        instance.save()

@receiver(post_save, sender=User)
def create_profile_for_new_user(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
