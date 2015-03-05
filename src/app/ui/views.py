# -*- coding: utf-8 -*-

from decorators import render_to
from settings import PROGRAM_VERSION
from django.template.loader import render_to_string
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.conf import settings

@render_to('ui/index.html')
def index(request):
    return {'PROGRAM_VERSION':PROGRAM_VERSION}

@login_required
def traceback(request):
    if request.method == "POST":
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

@login_required
@render_to('ui/report.html')
def report(request):
    return {
        'settings': settings
    }

@login_required
@render_to('ui/abonlist.html')
def abonlist(request):
    from app.abon.models import Building
    lines = []
    for b in Building.objects.all():
        l = []
        for a in b.addresses.all().order_by('flat'):
            for ab in a.abonents.all():
                if ab.disabled:
                    continue
                if ab.cards.count()>1:
                    l.append("&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;%s (&#1062;&#1080;&#1092;&#1088;&#1072;)" % (a.flat or "","%s" % ab.person.fio_short()))
                else:
                    l.append("&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;%s" % (a.flat or "","%s" % ab.person.fio_short()))
        if len(l):
            lines.append(
                [b,l]
            )
    res = []

    for chapter in lines:
        header,ll = chapter
        res.append("")
        res.append("<b>%s</b>" % header)
        for l in ll:
            res.append(l)
    return {
        'lines':res
    }

@login_required
@render_to('ui/abonlist.html')
def abonlist_c(request):
    from app.abon.models import Building
    lines = []
    for b in Building.objects.all():
        l = []
        for a in b.addresses.all().order_by('flat'):
            for ab in a.abonents.all():
                if ab.disabled:
                    continue
                l.append("&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;%s" % (a.flat or "","%s" % ab.person.fio_short()))
        if len(l):
            lines.append(
                [b,l]
            )
    res = []

    for chapter in lines:
        header,ll = chapter
        res.append("")
        res.append("<b>%s</b>" % header)
        for l in ll:
            res.append(l)
    return {
        'lines':res
    }

@login_required
@render_to('ui/abonlist.html')
def abonlist_d(request):
    from app.abon.models import Building
    lines = []
    for b in Building.objects.all():
        l = []
        for a in b.addresses.all().order_by('flat'):
            for ab in a.abonents.all():
                if ab.disabled:
                    continue
                if ab.cards.count()>1:
                    l.append("&nbsp;&nbsp;&nbsp;%s&nbsp;&nbsp;%s (&#1062;&#1080;&#1092;&#1088;&#1072;)" % (a.flat or "","%s" % ab.person.fio_short()))
                else:
                    pass
        if len(l):
            lines.append(
                [b,l]
            )
    res = []

    for chapter in lines:
        header,ll = chapter
        res.append("")
        res.append("<b>%s</b>" % header)
        for l in ll:
            res.append(l)
    return {
        'lines':res
    }