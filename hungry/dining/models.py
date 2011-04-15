""" dining.models

Model classes that represent dining invitations/requests.

"""

from django.contrib.gis.db import models

from django.contrib.auth.models import User

class Invitation(models.Model):
    """ Invitation
    
    Represents an invitation to dine with a user.

    """

    # User who created the invitation
    user = models.ForeignKey(User, related_name='user_invitations')

    # Date/time of the invitation
    date_of = models.DateTimeField()

    # Location of the invitation
    location = models.PointField(srid=4326)
    
    # Maximum number of registered attendees
    max_attending = models.PositiveIntegerField()

    # Currently registered attendees of the invitation
    attendees = models.ManyToManyField(User, related_name='user_attending')

    # Creation timestamp
    created_at = models.DateTimeField(auto_now_add=True)

    # Last modified timestamp
    last_modified = models.DateTimeField(auto_now=True)


