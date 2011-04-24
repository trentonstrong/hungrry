import json
from datetime import date

from django.db import models
from django.contrib.auth.models import User
from django.utils.safestring import mark_safe
from django.dispatch import dispatcher
from django.db.models import signals
from django.template.defaultfilters import slugify

"""
media.models

Models related to media file storage
"""


class Media(models.Model):
    """
    Represents a single media file and any associated thumbnails/metadata
    """
    
    name = models.CharField(max_length = 255)

    url = models.URLField()

    thumbnail = models.URLField()

    mime_type = models.CharField(max_length = 128)

    metadata = models.TextField()

    created_at = models.DateTimeField(auto_now_add=True)

    last_modified = models.DateTimeField(auto_now=True)
    
    uploaded_by = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def media_tag(self):
        metadata = json.loads(self.metadata)
        return mark_safe('<img src="%s" width="%d" height="%d" alt="%s" />' % ( self.url, metadata['width'], metadata['height'], self.name ))

    def thumb_tag(self):
        metadata = json.loads(self.metadata)
        return mark_safe('<img src="%s" width="%d" height="%d" alt="%s" />' % ( self.thumbnail, 75, 75, self.name ))


class UserAlbum(models.Model):
    """ UserAlbum

    Organizes user media into separate albums for easy maintenance/browsing.

    """

    user = models.ForeignKey(User)

    name = models.CharField(max_length=50)

    slug = models.SlugField(max_length=100)

    is_public = models.BooleanField(default=True)

    media = models.ManyToManyField(Media)
    
    @classmethod
    def user_post_save(sender, instance, created, **kwargs):
        """ Creates default photo album for new user accounts """
        if created:
            instance.useralbum_set.create(
                name="Profile Pictures",
                is_public=True
            )
    
    @classmethod
    def album_pre_save(sender, instance, created, **kwargs):
        """ Handles pre album save actions, such as creating slugs """
        instance.slug = "%s-%s" % (date.today().isoformat(), instance.slugify(instance.name))



# Register signals
signals.post_save.connect(UserAlbum.user_post_save, sender=User)
