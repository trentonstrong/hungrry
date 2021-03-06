import os
import sys
import site

HOME = '/home/hungry/'
PROJECT_ROOT = os.path.join(HOME, 'hungrry')
CODE_ROOT = os.path.join(PROJECT_ROOT, 'hungry')
site_packages = os.path.join(HOME, '.virtualenvs/hungry/lib/python2.6/site-packages')
site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CODE_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hungry.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
