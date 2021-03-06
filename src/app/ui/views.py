# -*- coding: utf-8 -*-

from decorators import render_to
from settings import PROGRAM_VERSION
from django.template.loader import render_to_string
from django.http import HttpResponse

@render_to('ui/index.html')
def index(request):
    return {'PROGRAM_VERSION':PROGRAM_VERSION}


def traceback(request):
    if request.method == "POST":
        print request.POST
        traceback_text = request.POST.get('traceback',None)
        traceback_descr = request.POST.get('traceback-descr',None)
        context = {
            'USER_REPORTED':request.user,
            'PROGRAM_VERSION':PROGRAM_VERSION,
            'TRACEBACK_TEXT':traceback_text,
            'TRACEBACK_DESCR':traceback_descr,
        }
    else:
        context = {
            'PROGRAM_VERSION':PROGRAM_VERSION,
        }
    rendered = render_to_string('ui/traceback.html', context)
    
    from django.core.mail import EmailMultiAlternatives

    subject, from_email, to = 'BilTV crit error (%s)' % request.user, 'biltv@it-tim.net', 'mm@it-tim.net'
    text_content = 'BilTV crashreport:'
    html_content = rendered
    msg = EmailMultiAlternatives(subject, text_content, from_email, [to])
    msg.attach_alternative(html_content, "text/html")
    msg.send()

    return HttpResponse(rendered)

@render_to('ui/report.html')
def report(request):
    return {}