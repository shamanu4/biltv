from django.conf.urls.defaults import *

urlpatterns = patterns('data.views',
    url(r'^$', 'txt2sql', name='txt2sql'),
)