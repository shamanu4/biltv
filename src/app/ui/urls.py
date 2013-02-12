from django.conf.urls.defaults import *
from rpc import Router

router = Router()

urlpatterns = patterns('ui.views',
    url(r'^$', 'index', name='index'),
    url(r'^traceback/$', 'traceback', name='traceback'),
    url(r'^report/$', 'report', name='report'),
    url(r'^abonlist/$', 'abonlist', name='abonlist'),
    url(r'^abonlist/c/$', 'abonlist_c', name='abonlist_c'),
    url(r'^abonlist/d/$', 'abonlist_d', name='abonlist_d'),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),       
)