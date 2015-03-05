from django.conf.urls.defaults import *
from settings import STATIC_ROOT

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^biltv/', include('biltv.foo.urls')),

    # Uncomment the admin/doc line below and add 'django.contrib.admindocs' 
    # to INSTALLED_APPS to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),
    (r'^static/(?P<path>.*)$', 'django.views.static.serve',     
        {'document_root': STATIC_ROOT}),
    (r'^favicon.ico$', 'django.views.static.serve', 
        {'document_root': STATIC_ROOT, 'path':'favicon.ico'}),
    (r'^logs/admin/(?P<app_label>[^/]+)/(?P<model>[^/]+)/(?P<oid>\d+)/', 'logger.views.index'),
    (r'^admin/', include(admin.site.urls)),
    (r'^statements/', include('statements.urls', 'statements')),
    (r'^', include('ui.urls', 'ui')),
)
