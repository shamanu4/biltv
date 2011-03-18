# -*- coding: utf-8 -*-

from lib.extjs import store_read

class AbonApiClass(object):

    def foo(self,rdata,request):
        return dict(success=True, data=None)

    foo._args_len = 1

    def person_get(self, rdata, request):
        from abon.models import Abonent, Person
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
        if len(passport)>0:
            try:
                person=Person.objects.get(passport=passport)
            except Person.DoesNotExist:
                person=Person()
            else:
                pass
        elif uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                person = abonent.person        
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

    def abonent_get(self, rdata, request):
        from abon.models import Abonent
        try:
            a=Abonent.objects.get(pk=rdata['uid'])
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        else:
            return dict(success=True, data=[a.store_record()])
    abonent_get._args_len = 1

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

    def balance_get(self, rdata, request):
        from abon.models import Abonent
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки баланса', msg='abonent not found', errors='' )
            else:
                return dict(success=True, data={'balance':abonent.bill.balance} )
        else:
            return dict(success=True, data={'balance':None} )

    balance_get._args_len = 1

    @store_read
    def cards_get(self,rdata,request):
        from abon.models import Abonent
        try:
            uid = int(rdata['uid'])
        except KeyError:
            return dict(success=False, title='Сбой загрузки карт', msg='abonent not found', errors='' )
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки карт', msg='abonent not found', errors='' )
            else:                
                return abonent.card_set.all()
        else:
            return dict(success=True, data={} )

    cards_get._args_len = 1

    def cards_set(self,rdata,request):
        from abon.models import Abonent
        from tv.models import Card
        card_id = int(rdata['data']['num'])
        uid = int(rdata['uid'])
        if card_id>0 and uid>0:
            try:
                card=Card.objects.get(pk=card_id,owner__exact=None)
            except Card.DoesNotExist:
                return dict(success=False, title='Сбой загрузки тарифов', msg='card not found', errors='', data={} )
            else:
                try:
                    abonent=Abonent.objects.get(pk=uid)
                except Abonent.DoesNotExist:
                    return dict(success=False, title='Сбой загрузки карт', msg='abonent not found', errors='', data={} )
                else:
                    card.owner=abonent
                    card.save()
                    return dict(success=True, data=card.store_record() )
        else:
            return dict(success=True, data={} )
    cards_set._args_len = 1

    @store_read
    def free_cards_get(self,rdata,request):
        from tv.models import Card
        card=Card.objects.filter(num__gte=0,owner__exact=None)
        return card

    free_cards_get._args_len = 1

    @store_read
    def cards_tp_get(self,rdata,request):
        from tv.models import Card
        card_id = int(rdata['card_id'])
        if card_id>0:
            try:
                card=Card.objects.get(pk=card_id)
            except Card.DoesNotExist:
                return dict(success=False, title='Сбой загрузки тарифов', msg='card not found', errors='' )
            else:
                return card.services.all()
        else:
            return dict(success=True, data={} )

    cards_tp_get._args_len = 1

    def cards_tp_set(self,rdata,request):
        return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    cards_tp_set._args_len = 1

    @store_read
    def payments_get(self,rdata,request):
        from tv.models import Payment
        from abon.models import Abonent
        print rdata
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки платежей', msg='abonent not found', errors='', data={} )                    
        payments=Payment.objects.filter(bill=abonent.bill)
        return payments
    payments_get._args_len = 1


