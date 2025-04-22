from django.db.models.signals import post_save
from django.dispatch import receiver
from .models import Profile, CustomUser

@receiver(post_save, sender=CustomUser)
def create_user_profile(sender, instance, created, **kwargs):
    if created and not hasattr(instance, 'profile'):
        Profile.objects.create(user=instance)
        print(f"Profile created for user: {instance.email}")
    else:
        instance.profile.save()
        print(f"Profile updated for user: {instance.email}")