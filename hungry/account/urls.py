from django.conf.urls.defaults import *
from django.views.generic.simple import direct_to_template

from index.views import index

from registration.views import activate
from registration.views import register
from registration.forms import RegistrationFormTermsOfService

from account.views import profile

urlpatterns = patterns('',
                       # User Profile Pages
					   url(r'^profile/(?P<username>\w+)/$',
						   direct_to_template,
						   {'template': 'account/profile_display.html'},
						   name='user_details'),
                       
                       # User's own account profile
					   url(r'^profile/$',
						   profile,
						   name='account_profile'),
                       
                       # Activation completion page
                       url(r'^activate/complete/$',
                           direct_to_template,
                           {'template': 'registration/activation_complete.html'},
                           name='registration_activation_complete'),
                        
                       # Registration activation URL
                       # Activation keys get matched by \w+ instead of the more specific
                       # [a-fA-F0-9]{40} because a bad activation key should still get to the view;
                       # that way it can return a sensible "invalid key" message instead of a
                       # confusing 404.
                       url(r'^activate/(?P<activation_key>\w+)/$',
                           activate,
                           {'backend': 'registration.backends.default.DefaultBackend'},
                           name='registration_activate'),
                       
                       # User registration form
                       url(r'^register/$',
                           register,
						   {'backend': 'registration.backends.default.DefaultBackend',
							'form_class': RegistrationFormTermsOfService},
                           name='registration_register'),

                       # Registration complete page
                       url(r'^register/complete/$',
                           direct_to_template,
                           {'template': 'registration/registration_complete.html'},
                           name='registration_complete'),
                       
                       # Registration Closed Page (if registration is turned off)
                       url(r'^register/closed/$',
                           direct_to_template,
                           {'template': 'registration/registration_closed.html'},
                           name='registration_disallowed'),

                       (r'', include('registration.auth_urls')),
                       )
