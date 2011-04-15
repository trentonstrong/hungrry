from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from hungry.media.views import user_media, user_album

urlpatterns = patterns('',
                        url(r'^(?P<username>\w+)/$',
                            user_media,
                            name='user_media'),

                        url(r'^(?P<username>\w+)/(?P<albumid>\d+)/$',
                            user_album,
                            name='user_album'),
                        )
