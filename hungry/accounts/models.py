import os
import hashlib

from django.db import models
from django.contrib.auth.models import User

from hungry import settings

from hungry.media.models import Media, UserAlbum



# Sitewide profile for users.  Extends basic user data with application specifics (like location data)
class UserProfile(models.Model):

        default_image_path = '%simages/default_image.gif' % settings.STATIC_URL

        user = models.OneToOneField(User)

        zip_code = models.CharField(max_length = 9)

        avatar = models.ForeignKey(Media, null = True)

        profile_album = models.ForeignKey(UserAlbum, null = True)
