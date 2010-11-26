# To change this template, choose Tools | Templates
# and open the template in the editor.

from extjs import store_read

class TvApiClass(object):

    @store_read
    def channels(self):
        from tv.models import Channel
        return Channel.objects.all()
