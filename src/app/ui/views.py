# -*- coding: utf-8 -*-

from decorators import render_to
from settings import PROGRAM_VERSION

@render_to('ui/index.html')
def index(request):
    return {'PROGRAM_VERSION':PROGRAM_VERSION}
