from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template, redirect_to

from hungry.index.views import index

from registration.views import activate
from registration.views import register
from registration.forms import RegistrationFormTermsOfService

from hungry.accounts.views import profile, profile_photo

urlpatterns = patterns('',
                       url(r'^$',
                           redirect_to,
                           {'url': 'profile/' }),

                       # User Profile Pages
					   url(r'^profile/(?P<username>\w+)/$',
						    profile,
						   name='user_profile'),
                       
                       # User's own accounts profile
					   url(r'^profile/$',
						   profile,
						   name='self_profile'),
                       
                       # URL for retrieving/setting user profile photo
                       # Currently a callback endpoint for Transloadit upload service
                       url(r'^profile/(?P<username>\w+)/photo$',
                           profile_photo,
                           name='account_profile_photo'),
                
                       (r'', include('registration.urls')),
                       )
