# -*- coding: utf-8 -*-

from django import forms
from django.db.utils import IntegrityError

class CityForm(forms.Form):
    name = forms.CharField(required=True)
    label = forms.CharField(required=False)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)

    def save(self,obj=None):
        from abon.models import City
        if not obj:
            obj = City()
        obj.name = self.cleaned_data['name']
        obj.label = self.cleaned_data['label']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')

class StreetForm(forms.Form):
    pass