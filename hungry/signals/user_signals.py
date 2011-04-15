""" Signals related to events in the auth/user module """

from django.dispatch import receiver
from django.db.models.signals import post_save
from django.contrib.auth.models import User

from hungry.media.models import UserAlbum

@receiver(post_save, sender=User)
def user_post_save(sender, **kwargs):
    # Create default photo album
    sender.useralbum_set.create(
        name="Profile Pictures",
        is_public=true
    )
