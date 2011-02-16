# -*- coding: utf-8 -*-

from django import forms
from django.db.utils import IntegrityError

class CityForm(forms.Form):
    name = forms.CharField(required=True, max_length=40)
    label = forms.CharField(required=False, max_length=40)
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
    city = forms.IntegerField(required=True)
    name = forms.CharField(required=True, max_length=40)
    code = forms.CharField(required=True, max_length=5)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)

    def clean_city(self):
        from abon.models import City
        city = self.cleaned_data['city']
        try:
            city=City.objects.get(pk=city)
        except City.DoesNotExist:
            raise forms.ValidationError("City related object not exists.")
        return city

    def save(self,obj=None):
        from abon.models import Street
        if not obj:
            obj = Street()
        obj.city = self.cleaned_data['city']
        obj.name = self.cleaned_data['name']
        obj.code = self.cleaned_data['code']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')

class HouseNumForm(forms.Form):
    num = forms.CharField(required=True, max_length=40)
    code = forms.CharField(required=True, max_length=5)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)

    def save(self,obj=None):
        from abon.models import House
        if not obj:
            obj = House()
        obj.num = self.cleaned_data['num']
        obj.code = self.cleaned_data['code']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')

class BuildingForm(forms.Form):
    street = forms.IntegerField(required=True)
    house = forms.IntegerField(required=True)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)
    
    def clean_street(self):
        from abon.models import Street
        street = self.cleaned_data['street']
        try:
            street=Street.objects.get(pk=street)
        except Street.DoesNotExist:
            raise forms.ValidationError("Street related object not exists.")
        return street
    
    def clean_house(self):
        from abon.models import House
        house = self.cleaned_data['house']
        try:
            house=House.objects.get(pk=house)
        except House.DoesNotExist:
            raise forms.ValidationError("House related object not exists.")
        return house

    def save(self,obj=None):
        from abon.models import Building
        if not obj:
            obj = Building()
        obj.street = self.cleaned_data['street']
        obj.house = self.cleaned_data['house']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')

