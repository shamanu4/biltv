from django.conf.urls.defaults import *
from rpc import Router

router = Router()

urlpatterns = patterns('statements.views',
    url(r'^$', 'index', name='index'),
    url(r'^(?P<day>\d{4}\-\d{2}\-\d{2})$', 'statement', name='statement'),
    url(r'^upload/$', 'upload', name='upload'),
    # url(r'^traceback/$', 'traceback', name='traceback'),
    # url(r'^report/$', 'report', name='report'),
    # url(r'^abonlist/$', 'abonlist', name='abonlist'),
    # url(r'^abonlist/c/$', 'abonlist_c', name='abonlist_c'),
    # url(r'^abonlist/d/$', 'abonlist_d', name='abonlist_d'),
    url(r'^router/$', router, name='router'),
    url(r'^router/api/$', router.api, name='api'),
)