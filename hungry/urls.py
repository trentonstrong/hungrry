from django.conf.urls.defaults import *
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from hungry.index.views import index

# Uncomment the next two lines to enable the admin:
# from django.contrib import admin
# admin.autodiscover()

urlpatterns = patterns('',
    # Example:
	url(r'^$',
		index,
		name='homepage'),

    url(r'^accounts/',
	    include('hungry.accounts.urls')),

    url(r'^media/',
        include('hungry.media.urls')),
        

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    # Uncomment the next line to enable the admin:
    # (r'^admin/', include(admin.site.urls)),
)

urlpatterns += staticfiles_urlpatterns()
