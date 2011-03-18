# -*- coding: utf-8 -*-

from django.template import Context, loader
from django.contrib.contenttypes.models import ContentType
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.utils import simplejson

@login_required

def index(request,app_label,model,oid):
    from logger.models import Log    

    try:
        content_type = ContentType.objects.get(app_label=app_label, model=model)
    except ContentType.DoesNotExist:
        log = {}
        object='unknown object'
    else:
        log = Log.objects.filter(content_type=content_type,oid=oid)
        try:
            object = content_type.get_object_for_this_type(pk=oid)
        except ObjectDoesNotExist:
            object='unknown object'

    for entry in log:
        entry.data = simplejson.loads(str(entry.data))

    c = Context({'log_entires':log,'app_label':app_label,'module_name':model,'object':object,'oid':oid,})
    t = loader.get_template('admin/object_log.html')

    return HttpResponse(t.render(c))
