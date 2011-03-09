import json

from django.db import models
from django.utils.safestring import mark_safe

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

    def media_tag(self):
        metadata = json.loads(self.metadata)
        return mark_safe('<img src="%s" width="%d" height="%d" alt="%s" />' % ( self.url, metadata['width'], metadata['height'], self.name ))

    def thumb_tag(self):
        metadata = json.loads(self.metadata)
        return mark_safe('<img src="%s" width="%d" height="%d" alt="%s" />' % ( self.thumbnail, 75, 75, self.name ))
