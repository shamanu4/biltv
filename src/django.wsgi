import os, sys
sys.path.append('/usr/local/etc/django')
sys.path.append('/usr/local/etc/django/biltv')
os.environ['DJANGO_SETTINGS_MODULE'] = 'biltv.settings'

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()
