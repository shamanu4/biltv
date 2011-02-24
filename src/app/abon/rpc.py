# -*- coding: utf-8 -*-

from extjs import store_read
from django.db.utils import IntegrityError

class AbonApiClass(object):
    def person_get(self, rdata, request):
        from abon.models import Abonent,Person
        from lib.functions import latinaze
        
        if 'uid' in rdata:
            uid = int(rdata['uid'])
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                return dict(success=True, data=abonent.person.store_record())

        elif 'passport' in rdata:
            try:
                person=Person.objects.get(passport=latinaze(rdata['passport']))
            except Person.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', errors='')
            else:
                return dict(success=True, data=person.store_record())

        else:
            return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')        
        

    person_get._args_len = 1

    def person_set(self, rdata, request):
        from abon.models import Abonent, Person
        from abon.forms import PersonForm
        from lib.functions import latinaze
        uid = int(rdata.__getitem__('uid'))
        passport = rdata.__getitem__('passport')
        passport = latinaze(passport)
        if not passport:
            return dict(success=False, title='Неправильный номер паспорта', msg='passport number is invalid', errors='')
        if uid>0:
            print 'editing person'
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                person = abonent.person
        elif len(passport)>0:
            print 'trying get person by passport'
            try:
                person=Person.objects.get(passport=passport)
            except Person.DoesNotExist:
                print 'failed'
                person=Person()
            else:
                print 'success'
        else:
            person=Person()

        form = PersonForm(rdata)
        result = []
        
        if form.is_valid():
            res = form.save(person)
            ok = res[0]
            result.append(res[1].store_record())
            msg = res[2]
        else:
            ok = False
            msg = form._errors
        if ok:
            return dict(success=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})        

    person_set._form_handler = True

    def address_get(self, rdata, request):
        from abon.models import Abonent
        try:
            a=Abonent.objects.get(pk=rdata['uid'])
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        else:
            return dict(success=True, data=a.address.store_record())

    address_get._args_len = 1

    def address_set(self, rdata, request):
        from abon.models import Abonent, Address
        from abon.forms import AddressForm
        uid = int(rdata.__getitem__('uid'))
        print uid
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                address = abonent.address
        else:
            address=Address()

        form = AddressForm(rdata)
        result = []

        if form.is_valid():
            res = form.save(address)
            ok = res[0]
            result.append(res[1].store_record())
            msg = res[2]
        else:
            ok = False
            msg = form._errors
        if ok:
            return dict(success=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})

    address_set._form_handler = True

    def abonent_set(self, rdata, request):
        from abon.models import Abonent
        from abon.forms import AbonentForm
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        else:
            abonent = Abonent()

        form = AbonentForm(rdata)
        result = []

        if form.is_valid():
            res = form.save(abonent)
            ok = res[0]
            result.append(res[1].store_record())
            msg = res[2]
        else:
            ok = False
            msg = form._errors
        if ok:
            return dict(success=True, title="Сохранено", msg="saved", data=result)
        else:
            return dict(success=False, title="Ошибка записи !!!", msg=msg, data={})

    abonent_set._args_len = 1
