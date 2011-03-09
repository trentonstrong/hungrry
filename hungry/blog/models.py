from django.db import models


class Post(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateTimeField()
    body = models.TextField()
    published = models.BooleanField(default=True)

    def __unicode__(self):
        return self.title
