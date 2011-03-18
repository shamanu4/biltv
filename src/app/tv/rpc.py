# -*- coding: utf-8 -*-

from lib.extjs import store_read

class TvApiClass(object):

    @store_read
    def channels(self,request):
        from tv.models import Channel
        return Channel.objects.all()
