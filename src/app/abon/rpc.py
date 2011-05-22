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
	    if a.deactivated: 
	        data.update({'deactivated':a.deactivated.date()}) #страшний бидлокод.2
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
                a=Abonent.objects.get(code__iexact=rdata['code'],disabled__exact=False)
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
                return abonent.cards.all()
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
        return PaymentRegister.objects.all().order_by('closed').order_by('-start')[:20]
    
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
        
        pr = Payment.objects.latest('id')
        pt = Payment.objects.filter(id__gte=pr.id-5,bill=abonent.bill)
        if pt.count()>0:
            return dict(success=False, title='Сбой проведения оплаты', msg='Возможно повторный ввод квитанции', errors='', data={} )
        
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
        from datetime import datetime, timedelta
                
        if 'start_date' in rdata and rdata['start_date']>0:
            start_date = rdata['start_date']
            try:
                start_date = datetime.strptime(start_date,'%Y-%m-%dT%H:%M:%S').date()
            except ValueError:
                return dict(success=False, title='Сбой получения статистики оплат', msg='invalid date', errors='', data={} )
        else:
            start_date = None
            
        if 'end_date' in rdata and rdata['end_date']>0:
            end_date = rdata['end_date']
            try:
                end_date = datetime.strptime(end_date,'%Y-%m-%dT%H:%M:%S').date()+timedelta(days=1)
            except ValueError:
                return dict(success=False, title='Сбой получения статистики оплат', msg='invalid date', errors='', data={} ) 
        else:
            end_date = None
            start_date = None
        print start_date
        print end_date        
        
        if 'register_id' in rdata and rdata['register_id']>0:            
            try:
                register = PaymentRegister.objects.get(pk=rdata['register_id'])
            except PaymentRegister.DoesNotExist:
                return dict(success=False, title='Сбой получения статистики оплат', msg='register not found', errors='', data={} )        
        else:
            register = None
        
        if 'admin_id' in rdata and rdata['admin_id']>0:            
            try:
                admin = User.objects.get(pk=rdata['admin_id'])
            except User.DoesNotExist:
                return dict(success=False, title='Сбой получения статистики оплат', msg='operator not found', errors='', data={} )
        else:
            admin = None
        
        if not register and not start_date:
            return dict(success=False, title='Сбой получения статистики оплат', msg='выберите реестр или интервал', errors='', data={} )
        
        payments = None
        
        if not register == None:                            
            payments = Payment.objects.filter(register=register)
                
        if not start_date == None:
            if not payments == None:
                payments = payments.filter(timestamp__gte=start_date).filter(timestamp__lte=end_date)
            else:
                payments = Payment.objects.filter(timestamp__gte=start_date).filter(timestamp__lte=end_date)
                
        if admin:
            payments = payments.filter(admin=admin)
        
        sum = payments.aggregate(current=models.Sum('sum'))['current'] or 0
        count = payments.count()
        
        return (payments,{'sum':sum,'count':count})    
    
    reg_payments_get._args_len = 1
        
    def reg_payments_delete(self,rdata,request):
        from tv.models import Payment
        if 'payment_id' in rdata and rdata['payment_id']>0:
            payment_id = rdata['payment_id']
            try:
                payment = Payment.objects.get(pk=payment_id)
            except Payment.DoesNotExist:
                return dict(success=False, title='Сбой удаления оплат', msg='payment not found', errors='', data={} )
            else:                
                if payment.maked:
                    return dict(success=False, title='Сбой удаления оплат', msg='платёж уже засчитан', errors='', data={} )
                else:
                    payment.delete()
                    return dict(success=True, title='Оплата удалена', msg='deleted', errors='', data={} )
        else:
            return dict(success=False, title='Сбой удаления оплат', msg='payment not found', errors='', data={} )
        
    reg_payments_delete._args_len = 1
    
    def reg_payments_partially_confirm(self,rdata,request):
        from tv.models import PaymentRegister
        if 'register_id' in rdata and rdata['register_id']>0:
            register_id = rdata['register_id']
            try:
                register = PaymentRegister.objects.get(pk=register_id)
            except PaymentRegister.DoesNotExist:
                return dict(success=False, title='Сбой подтверждение платежей', msg='register not found', errors='', data={} )
            else:                
                if register.closed:
                    return dict(success=False, title='Сбой подтверждение платежей', msg='реестр закрыт', errors='', data={} )
                else:
                    payments = register.payments.filter(maked__exact=False,deleted__exact=False)
                    count = payments.count()
                    for payment in payments:
                        payment.make()
                    return dict(success=True, title='Подтверждение платежей', msg='подтверждено: %s' % count, errors='', data={} )
        else:
            return dict(success=False, title='Сбой подтверждение платежей', msg='register not found', errors='', data={} )
        
    reg_payments_partially_confirm._args_len = 1
                    
    @store_read
    def admins_get(self,rdata,request):
        from accounts.models import User
    
        return User.objects.all()
    
    admins_get._args_len = 1
    
    def comment_get(self,rdata,request):
        from abon.models import Abonent
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки ', msg='abonent not found', errors='' )
            else:
                return dict(success=True, data={'comment':abonent.comment} )
        else:
            return dict(success=True, data={'comment':None} )
        
    comment_get._args_len = 1
    
    def comment_set(self,rdata,request):
        from abon.models import Abonent
        if not 'uid' in rdata or not 'comment' in rdata:
            return dict(success=False, title='Сбой записи коментария', msg='invalid parameters', errors='' )
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой записи коментария', msg='abonent not found', errors='' )
            else:
                abonent.comment=rdata['comment']
                abonent.save()
                return dict(success=True, title='Сохранено', msg='saved', errors='' )
        else:
            return dict(success=False, title='Сбой загрузки ', msg='abonent not found', errors='' )
        
    comment_set._args_len = 1
        
