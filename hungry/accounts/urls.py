from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from hungry.index.views import index

from registration.views import activate
from registration.views import register
from registration.forms import RegistrationFormTermsOfService

from hungry.accounts.views import profile, profile_update, profile_photo

urlpatterns = patterns('',
                       # User Profile Pages
					   url(r'^profile/(?P<username>\w+)/$',
						   direct_to_template,
						   {'template': 'accounts/profile_display.html'},
						   name='user_details'),
                       
                       # User's own accounts profile
					   url(r'^profile/$',
						   profile,
						   name='account_profile'),

                       # Update user profile
                       url(r'^profile/update$',
                           profile_update,
                           name='account_profile_update'),
                       
                       # URL for retrieving/setting user profile photo
                       # Currently a callback endpoint for Transloadit upload service
                       url(r'^profile/(?P<username>\w+)/photo$',
                           profile_photo,
                           name='account_profile_photo'),
                
                       (r'', include('registration.urls')),
                       )
