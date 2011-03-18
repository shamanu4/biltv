# -*- coding: utf-8 -*-

from decorators import render_to

@render_to('ui/index.html')
def index(request):
    return {}
