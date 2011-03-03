# -*- coding: utf-8 -*-

from django import forms
from django.db.utils import IntegrityError

class CardForm(forms.Form):

    num = forms.IntegerField(required=True)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)
        
    def save(self,obj=None):
        from tv.models import Card
        if not obj:
            obj = Card()

        obj.num = self.cleaned_data['num']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')