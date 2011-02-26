from django.db import models
from django.contrib.auth.models import User
from sorl.thumbnail.fields import ThumbnailField
import settings

import os
import hashlib

# Returns the media upload path for a user
#
# The path itself is the md5 hash of the site secret key + the username.  Not meant to be totally crypto-secure, just sufficiently unique/obfuscated.
def get_user_upload_dir(instance, filename):
		upload_dir = None

		if (instance.upload_dir):
				upload_dir = instance.upload_dir
		else:
				secret_key = settings.SECRET_KEY
				username = self.user.username

				md5_hasher = hashlib.md5()
				md5_hasher.update(secret_key)
				md5_hasher.update(username)
				md5_hex = md5_hasher.hexdigest()
				
				user_prefix = settings.USER_UPLOAD_PREFIX
				
				# upload folder (relative to media root) is ~/user_prefix/md5_hex
				upload_dir = '%s%s' % (user_prefix, md5_hex)
		
		return upload_dir


# Sitewide profile for users.  Extends basic user data with application specifics (like location data)
class UserProfile(models.Model):

		default_image_path = '%simages/default_image.gif' % settings.STATICFILES_URL

		user = models.ForeignKey(User, unique=True)

		zip_code = models.CharField(max_length = 5)

		upload_dir = models.CharField(max_length = 100, blank = True)

		profile_image = ThumbnailField(
						upload_to = get_user_upload_dir,
						default = default_image_path,
						size = (100,100),
						)

		

