# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from decorators import render_to
from settings import PROGRAM_VERSION
from django.http import HttpResponse, HttpResponseRedirect
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.core.management import call_command
from datetime import date, datetime
import json
import os
import errno
from subprocess import Popen, PIPE
from .forms import XLSUploadForm

PATH = "/home/maxim/projects/biltv2/src/app/statements/tmp"


def index(request):
    return HttpResponseRedirect(reverse("statements:statement", kwargs={'day': date.today().strftime("%Y-%m-%d")}))


@render_to('statements/index.html')
def statement(request, day):
    return {
        'PROGRAM_VERSION':PROGRAM_VERSION,
        'day': day
    }


def mkdir_p(path):
    try:
        os.makedirs(path)
    except OSError as exc: # Python >2.5
        if exc.errno == errno.EEXIST and os.path.isdir(path):
            pass
        else:
            raise


def handle_uploaded_file(f, day):
    dir = "%s/%s/%s" % (PATH, day.year, day.month)
    mkdir_p(dir)
    daystr = day.strftime("%Y-%m-%d")
    path = '%s/%s.xls' % (dir, daystr)
    with open(path, 'wb+') as destination:
        for chunk in f.chunks():
            destination.write(chunk)
    process(path, daystr)


def process(path, daystr):
    p = Popen(['python', 'manage.py', 'import_xls', path, daystr, '--process'], stdout=PIPE, stderr=PIPE)
    output = p.communicate()
    if output[1]:
        raise RuntimeError(output[1])


@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = XLSUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['xls'], form.cleaned_data['day'])
            except Exception, e:
                resp = {
                    "success": False,
                    "errors": str(e)
                }
            else:
                resp = {
                    "success": True,
                    "msg": 'file uploaded'
                }
        else:
            resp = {
                "success": False,
                "errors": json.dumps(form.errors)
            }
        return HttpResponse(json.dumps(resp))