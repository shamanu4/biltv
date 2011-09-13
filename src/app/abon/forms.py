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


class PersonForm(forms.Form):
    firstname = forms.CharField(required=True, max_length=40)
    lastname = forms.CharField(required=True, max_length=40)
    middlename = forms.CharField(required=True, max_length=40)
    passport = forms.CharField(required=True, max_length=20)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)

    def save(self,obj):
        from abon.models import Person
        if not obj:
            obj = Person()
        obj.firstname = self.cleaned_data['firstname']
        obj.lastname = self.cleaned_data['lastname']
        obj.middlename = self.cleaned_data['middlename']
        obj.passport = self.cleaned_data['passport']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')


class AddressForm(forms.Form):

    street = forms.CharField(required=True, max_length=40)
    house = forms.CharField(required=True, max_length=40)
    flat = forms.CharField(required=True, max_length=40)
    ext = forms.CharField(required=True, max_length=20)
    deleted = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)
    
    def save(self,obj):
        print self.cleaned_data
        from abon.models import Address,Building
        if not obj:
            obj = Address()
        b = Building()
        b = b.get_or_create(self.cleaned_data['street'],self.cleaned_data['house'])
        try:
            b.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        obj = obj.get_or_create(b,self.cleaned_data['flat'],self.cleaned_data['ext'])
        #obj.code = self.cleaned_data['ext'] or ''
        obj.code = ''
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.comment = self.cleaned_data['comment']
        try:
            obj.save()
        except IntegrityError as error:
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,'')


class AbonentForm(forms.Form):

    person_id = forms.IntegerField(required=True)
    address_id = forms.IntegerField(required=True)
    deleted = forms.BooleanField(required=False)
    confirmed = forms.BooleanField(required=False)
    activated = forms.DateTimeField(required=False)
    deactivated = forms.DateTimeField(required=False)
    disabled = forms.BooleanField(required=False)
    comment = forms.CharField(required=False)

    def save(self,obj=None):
        from abon.models import Address,Person,Abonent
                
        try:
            address = Address.objects.get(pk=self.cleaned_data['address_id'])
        except Address.DoesNotExist:
            return (False,obj,'address not found')
        try:
            person = Person.objects.get(pk=self.cleaned_data['person_id'])
        except Person.DoesNotExist:
            return (False,obj,'person not found')
        
        msg=''
        print "---1"
        print obj
        if obj and obj.pk:
            pass
            print 'obj!'
        else:
            print 'not obj'
            try: 
                obj = Abonent.objects.get(person=person,address=address)
            except Abonent.DoesNotExist:
                pass
                print 'not exist'
                print person
                print address
                obj = Abonent(disabled=True)
            else:
                print 'exists'
                msg='Абонент существует... режим редактирования включён...'            
                            
                
        obj.person = person
        obj.address = address
        #obj.activated = self.cleaned_data['activated']
        #obj.deactivated = self.cleaned_data['deactivated']
        obj.deleted = self.cleaned_data['deleted'] or False
        obj.confirmed = self.cleaned_data['confirmed'] or False
        obj.comment = self.cleaned_data['comment']
        print obj
        print self.cleaned_data
        try:
            obj.save()
        except IntegrityError as error:
            print 'integrity error'
            return (False,obj,error[1].decode('utf8'))
        else:
            return (True,obj,msg)