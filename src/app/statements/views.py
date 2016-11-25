# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from decorators import render_to
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
from .models import Statement

from django.conf import settings
import traceback

PROGRAM_VERSION = settings.PROGRAM_VERSION
PATH = settings.STATEMENTS_PATH
PROJECT_ROOT = settings.PROJECT_ROOT


def index(request):
    return HttpResponseRedirect(reverse("statements:statement", kwargs={'day': date.today().strftime("%Y-%m-%d")}))


@render_to('statements/index.html')
def statement(request, day):
    try:
        statement_id = Statement.objects.get(day=day).pk
    except Statement.DoesNotExist:
        statement_id = 0
    return {
        'PROGRAM_VERSION':PROGRAM_VERSION,
        'day': day,
        'statement_id': statement_id
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
    p = Popen(['python', '%s/manage.py' % PROJECT_ROOT, 'import_xls', path, daystr, '--process'], stdout=PIPE, stderr=PIPE)
    out, err = p.communicate()
    if err:
        raise RuntimeError(err)


@login_required
@csrf_exempt
def upload(request):
    if request.method == 'POST':
        form = XLSUploadForm(request.POST, request.FILES)
        if form.is_valid():
            try:
                handle_uploaded_file(request.FILES['xls'], form.cleaned_data['day'])
            except Exception:
                resp = {
                    "success": False,
                    "errors": traceback.format_exc().splitlines()
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