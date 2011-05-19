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


class RegisterForm(forms.Form):
    
    source = forms.IntegerField(required=True)
    total = forms.FloatField(required=True)
    closed = forms.BooleanField(required=False)
    start = forms.DateField(required=True)
    end = forms.DateField(required=True)
    bank = forms.DateField(required=True)
    
    def __init__(self,rdata):
        import re
        r = re.compile('(\d{4}\-\d{2}-\d{2}).*')
        rtst = r.match(rdata['start'])
        if rtst:
            rdata['start'] = rtst.group(1)
        rtst = r.match(rdata['end'])
        if rtst:
            rdata['end'] = rtst.group(1)
        rtst = r.match(rdata['bank'])
        if rtst:
            rdata['bank'] = rtst.group(1)
        super(self.__class__, self).__init__(rdata)
        
        
    def clean_source(self):
        from tv.models import PaymentSource
        try:
            source = PaymentSource.objects.get(pk=self.cleaned_data['source'])
        except PaymentSource.DoesNotExist:
            raise forms.ValidationError("Source related object not exists.")
        return source
    
    def save(self,obj=None):
        from tv.models import PaymentRegister
        if not obj:
            obj = PaymentRegister()
        
        obj.source = self.cleaned_data['source']    
        obj.total = self.cleaned_data['total']
        obj.closed = self.cleaned_data['closed'] or False
        obj.start = self.cleaned_data['start']
        obj.end = self.cleaned_data['end']
        obj.bank = self.cleaned_data['bank']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')        