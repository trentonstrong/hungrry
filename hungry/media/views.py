"""
Views for the media application
"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required

from django.contrib.auth.models import User
from hungry import settings
from hungry.media.models import Media, UserAlbum

def user_media(request, username):
    """ Displays a user's albums """
    owner = User.objects.get(username=username)
    albums = owner.useralbum_set.all()

    return render_to_response('media/user_media_all.html',
                               {'owner': owner,
                                'albums': albums},
                                context_instance=RequestContext(request))

def user_album(request, username, albumid):
    """ Displays a particular user album """
    owner = User.objects.get(username=username)
    album = owner.useralbum_set.select_related().get(id=albumid)

    return render_to_response('media/user_album.html',
                              {'owner': owner,
                               'album': album},
                               context_instance=RequestContext(request))
