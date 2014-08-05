# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django import forms

class XLSUploadForm(forms.Form):
    day = forms.DateField()
    xls = forms.FileField()