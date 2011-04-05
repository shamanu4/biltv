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
            data = a.address.store_record()
            data.update({'activated':a.activated.date()}) #страшний бидлокод. 
            return dict(success=True, data=data)

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
        print rdata
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
        if 'uid' in rdata and rdata['uid']>0:
            try:
                a=Abonent.objects.get(pk=rdata['uid'])
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                return dict(success=True, data=[a.store_record()])
        elif 'code' in rdata:
            try:
                a=Abonent.objects.get(code__iexact=rdata['code'])
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            else:
                return dict(success=True, data=[a.store_record()])
        else:
            return dict(success=False, errors='')
            #return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        
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
        print rdata
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
            return payments.order_by('-timestamp')
        return {}
    payments_get._args_len = 1

    @store_read
    def fees_get(self,rdata,request):
        from tv.models import Fee
        from abon.models import Abonent
        print rdata
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки платежей', msg='abonent not found', errors='', data={} )                    
            fees=Fee.objects.filter(bill=abonent.bill)
            return fees.order_by('-timestamp')
        return {}
    fees_get._args_len = 1
    
    @store_read
    def registers_get(self,rdata,request):
        from tv.models import PaymentRegister
        return PaymentRegister.objects.filter(closed__exact=False)
    
    registers_get._args_len = 1
    
    @store_read
    def registers_get_last(self,rdata,request):
        from tv.models import PaymentRegister
        return PaymentRegister.objects.all().order_by('-timestamp')[:20]
    
    registers_get_last._args_len = 1
    
    def make_payment(self,rdata,request):
        from tv.models import PaymentRegister, Payment
        from abon.models import Abonent
        from datetime import datetime
        
        print rdata
        
        register_id = int(rdata['register'])
        uid = int(rdata['abonent'])
        sum = float(rdata['sum'])
        tmpdate = rdata['bankdate']
        descr = rdata['descr'] or ''
        
        try:
            register = PaymentRegister.objects.get(pk=register_id)
        except PaymentRegister.DoesNotExist:
            return dict(success=False, title='Сбой проведения оплаты', msg='register not found', errors='', data={} )
        
        try:
            abonent = Abonent.objects.get(pk=uid)
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой проведения оплаты', msg='abonent not found', errors='', data={} )
        
        try:
            bank_date = datetime.strptime(tmpdate,'%Y-%m-%dT%H:%M:%S').date()
        except ValueError:
            return dict(success=False, title='Сбой проведения оплаты', msg='invalid date', errors='', data={} )    
        
        p = Payment()
        p.register = register
        p.source = register.source
        p.bill = abonent.bill
        p.sum = sum
        p.inner_descr = descr
        p.admin= request.user
        p.bank_date = bank_date
        p.save()
                    
        return dict(success=True, title='Оплата принята', msg='...', errors='', data={} )
    
    make_payment._args_len = 1
    
    @store_read    
    def feetypes_get(self,rdata,request):
        from tv.models import FeeType, FEE_TYPE_ONCE
        return FeeType.objects.filter(ftype=FEE_TYPE_ONCE)
    
    feetypes_get._args_len = 1
    
    def make_fee(self,rdata,request):
        from tv.models import FeeType, Fee
        from abon.models import Abonent
        from datetime import datetime
        
        print rdata
        
        ftype_id = int(rdata['type'])
        uid = int(rdata['abonent'])
        sum = float(rdata['sum'])
        tmpdate = rdata['bankdate']
        descr = rdata['descr'] or ''
        
        
        try:
            ftype = FeeType.objects.get(pk=ftype_id)
        except FeeType.DoesNotExist:
            return dict(success=False, title='Сбой снятия денег', msg='register not found', errors='', data={} )
        
        try:
            abonent = Abonent.objects.get(pk=uid)
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой снятия денег', msg='abonent not found', errors='', data={} )
        
        try:
            bank_date = datetime.strptime(tmpdate,'%Y-%m-%dT%H:%M:%S').date()
        except ValueError:
            return dict(success=False, title='Сбой снятия денег', msg='invalid date', errors='', data={} )    
        
        f = Fee()
        f.fee_type = ftype
        f.bill = abonent.bill
        f.sum = sum
        f.inner_descr = descr
        f.admin= request.user
        f.bank_date = bank_date
        f.save()
        f.make()
                    
        return dict(success=True, title='Снятие проведено', msg='...', errors='', data={} )        
    
    make_fee._args_len = 1

    @store_read    
    def reg_payments_get(self,rdata,request):
        from accounts.models import User
        from tv.models import Payment, PaymentRegister
        from django.db import models
        
        register_id = int(rdata['register_id'])
        
        if 'admin_id' in rdata and rdata['admin_id']>0:            
            try:
                admin = User.objects.get(pk=rdata['admin_id'])
            except User.DoesNotExist:
                return dict(success=False, title='Сбой получения статистики оплат', msg='operator not found', errors='', data={} )
        else:
            admin = None
        
        try:
            register = PaymentRegister.objects.get(pk=register_id)
        except PaymentRegister.DoesNotExist:
            return dict(success=False, title='Сбой получения статистики оплат', msg='register not found', errors='', data={} )
                                
        payments = Payment.objects.filter(register=register)
        
        if admin:
            payments = payments.filter(admin=admin)
        
        sum = payments.aggregate(current=models.Sum('sum'))['current'] or 0
        count = payments.count()
        
        return (payments,{'sum':sum,'count':count})    
    
    reg_payments_get._args_len = 1
    
    @store_read
    def admins_get(self,rdata,request):
        from accounts.models import User
    
        return User.objects.all()
    
    admins_get._args_len = 1
        