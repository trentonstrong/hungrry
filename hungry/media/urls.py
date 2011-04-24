from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from hungry.media.views import user_media, user_album, media_item

urlpatterns = patterns('',
                        url(r'^(?P<username>\w+)/$',
                            user_media,
                            name='user_media'),

                        url(r'^user/(?P<username>\w+)/album/(?P<slug>[\w-]+)/$',
                            user_album,
                            name='user_album'),

                        url(r'item/(?P<id>\d+/$',
                            media_item,
                            name='media_item'),
                        )
