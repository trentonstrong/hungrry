import os
import sys
import site

PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(os.path.dirname(__file__))))
CODE_ROOT = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
site_packages = os.path.join(PROJECT_ROOT, 'env/lib/python2.6/site-packages')
site.addsitedir(os.path.abspath(site_packages))
sys.path.insert(0, PROJECT_ROOT)
sys.path.insert(0, CODE_ROOT)
os.environ['DJANGO_SETTINGS_MODULE'] = 'hungry.settings'

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
