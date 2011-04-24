"""
Views for the media application
"""
from django.shortcuts import render_to_response, redirect
from django.template import RequestContext
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator, PageNotAnInteger, EmptyPage

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

def user_album(request, username, slug):
    """ Displays a particular user album """
    owner = User.objects.get(username=username)
    album = owner.useralbum_set.get(slug=slug)
    
    num_media_per_page = 10
    pager = Paginator(album.media.all(), num_media_per_page)

    page_number = request.GET.get('page', 1)
    try:
        page = pager.page(page_number)
    except PageNotAnInteger:
        page = pager.page(1)
    except EmtpyPage:
        page = pager.page(pager.num_pages)

    return render_to_response('media/user_album.html',
                              {'owner': owner,
                               'album': album,
                               'page': page},
                               context_instance=RequestContext(request))

def media_item(request, id):
    """ Displays a single media item """
    media = Media.objects.get(id=id)

    return render_to_response('media/media_item.html',
                                {},
                                context_instance=RequestContext(request))
    
