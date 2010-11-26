# -*- coding: utf-8 -*-

from decorators import render_to
import settings

@render_to('ui/index.html')
def index(request):
    return {}
    return {'MEDIA_URL':settings.MEDIA_URL}