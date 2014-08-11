# -*- encoding: utf-8 -*-
__author__ = 'maxim'

from django import forms
from .models import Entry


class XLSUploadForm(forms.Form):
    day = forms.DateField()
    xls = forms.FileField()


class EntryForm(forms.ModelForm):
    class Meta:
        model = Entry
