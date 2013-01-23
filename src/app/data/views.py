# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from decorators import render_to
from settings import PROGRAM_VERSION
from django.template.loader import render_to_string
from django.http import HttpResponse
from django import forms

class DataFileForm(forms.Form):
    table = forms.CharField(max_length=50)
    fields = forms.CharField(max_length=150)
    txt  = forms.FileField(required=False)

def handle_uploaded_file(f,table,fields):
    from django.db import connection
    cursor = connection.cursor()
    table = 'data_%s' % table
    ff = fields.split(';')
    cursor.execute("TRUNCATE TABLE %s" % table)
    chunk = ""
    errors = []
    for line in f:
        line = line.decode('windows-1251')
        line = "%s%s" % (chunk,line)
        chunk = ""
        if line.count('"') % 2:
            chunk = line
            continue
        data = line.split(";")
        clear_list = []
        for i,f in enumerate(ff):
            d = data[i].replace('\n', '').replace('\r', '')
            if d is None or d == '':
                clear_list.append('null')
            else:
                clear_list.append(d)
        query = "INSERT INTO %s VALUES (%s)" % (table,",".join(clear_list))
        print query
        try:
            cursor.execute(query)
        except Exception,e:
            errors.append((query,e))

@render_to('data/txt2sql.html')
def txt2sql(request):
    if request.method == 'GET':
        return {'form':DataFileForm()}
    if request.method == 'POST':
        f = DataFileForm(request.POST)
        if f.is_valid() and request.FILES:
            errs = handle_uploaded_file(request.FILES['txt'],f.cleaned_data['table'],f.cleaned_data['fields'])
            return {'errors':errs}
        else:
            return {'form':f}


