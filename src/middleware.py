# -*- coding: utf-8 -*-
from django.http import QueryDict

try:
    from threading import local
except ImportError:
    from django.utils._threading_local import local
from django.conf import settings

import json

def make_tls_property(default=None):
    """Creates a class-wide instance property with a thread-specific value."""
    class TLSProperty(object):
        def __init__(self):
            self.local = local()

        def __get__(self, instance, cls):
            if not instance:
                return self
            return self.value

        def __set__(self, instance, value):
            self.value = value

        def _get_value(self):
            return getattr(self.local, 'value', default)
        def _set_value(self, value):
            self.local.value = value
        value = property(_get_value, _set_value)

    return TLSProperty()

CURRENT_USER = settings.__class__.CURRENT_USER = make_tls_property()

class CurrentUserMiddleware(object):

    def process_request(self, request):
        if hasattr(request, 'user'):
            CURRENT_USER.value = request.user
        else:
            raise Exception('Put it after AuthenticateMiddleware')