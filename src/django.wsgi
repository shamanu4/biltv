import os, sys
sys.path.append('/usr/local/etc/django')
sys.path.append('/usr/local/etc/django/biltv')
sys.path.append('/usr/local/etc/django/biltv/src')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'
sys.stdout = sys.stderr

import django.core.handlers.wsgi

application = django.core.handlers.wsgi.WSGIHandler()