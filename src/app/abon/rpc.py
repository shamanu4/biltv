# -*- coding: utf-8 -*-

from lib.extjs import store_read, check_perm
from datetime import datetime

class AbonApiClass(object):

    @check_perm('accounts.rpc_abon_foo')
    def foo(self,rdata,request):
        return dict(success=True, data=None)

    foo._args_len = 1

    @check_perm('accounts.rpc_abon_person_get')
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

    @check_perm('accounts.rpc_abon_person_set')
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
            return dict(success=True, data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})        

    person_set._form_handler = True

    @check_perm('accounts.rpc_abon_address_get')
    def address_get(self, rdata, request):
        from abon.models import Abonent
        try:
            a=Abonent.objects.get(pk=rdata['uid'])
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        else:
            data = a.address.store_record()
        if a.activated: 
            data.update({'activated':a.activated.date()}) #страшний бидлокод.
        if a.deactivated: 
            data.update({'deactivated':a.deactivated}) #страшний бидлокод.2
        return dict(success=True, data=data)

    address_get._args_len = 1

    @check_perm('accounts.rpc_abon_address_set')
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
            return dict(success=True, data=result)
        else:
            return dict(success=False, title="Ошибка записи", msg=msg, data={})

    address_set._form_handler = True

    @check_perm('accounts.rpc_abon_abonent_get')
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
            a=Abonent.objects.filter(code__iexact=rdata['code'])
            if a.count()>1:
                a.filter(disabled__exact=False)
            if a.count()==0:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
            a = a[0]
            return dict(success=True, data=[a.store_record()])
        else:
            return dict(success=False, errors='')
            #return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        
    abonent_get._args_len = 1

    @check_perm('accounts.rpc_abon_abonent_get_by_code')
    @store_read
    def abonent_get_by_code(self, rdata, request):
        from abon.models import Abonent
        if 'code' in rdata:
            res =  Abonent.objects.filter(code__iexact=rdata['code']).order_by('disabled')
            if 'filter_disabled' in rdata and rdata['filter_disabled']:
                if not request.user.has_perm('abon.can_manage_disabled_abonents'):
                    res = res.filter(disabled__exact=False)
            return res
        else:
            return []
            #return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        
    abonent_get_by_code._args_len = 1

    @check_perm('accounts.rpc_abon_abonent_set')
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
            abonent = Abonent(disabled=True)
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
            return dict(success=True, title="Сохранено", msg=(msg or 'saved'), data=result)
        else:
            return dict(success=False, title="Ошибка записи !!!", msg=(msg or 'unknown error'), data={})

    abonent_set._args_len = 1

    @check_perm('accounts.rpc_abon_enable')
    def enable(self, rdata, request):
        from abon.models import Abonent
        from datetime import datetime        
        
        uid = int(rdata['abonent'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='ошибка включения', msg='abonent not found', errors='')
        
        other = Abonent.objects.filter(address__override__iexact=abonent.address.override, disabled__exact=False)
        if other.count()>0:
            return dict(success=False, title="ошибка включения", msg="Другой абонент включён по этому адресу")

        tmpdate = rdata['date']
        try:
            date = datetime.strptime(tmpdate,'%Y-%m-%dT%H:%M:%S').date()
        except ValueError:
            return dict(success=False, title='ошибка включения', msg='invalid date', errors='' )                    
        abonent.enable(date=date,descr=rdata['descr'])
        return dict(success=True, title="Абонент включен", msg="saved")

    enable._args_len = 1
    
    @check_perm('accounts.rpc_abon_disable')
    def disable(self, rdata, request):
        from abon.models import Abonent
        from datetime import datetime
        
        uid = int(rdata['abonent'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')

        tmpdate = rdata['date']
        try:
            date = datetime.strptime(tmpdate,'%Y-%m-%dT%H:%M:%S').date()
        except ValueError:
            return dict(success=False, title='Сбой отключения', msg='invalid date', errors='', data={} )                    
        abonent.disable(date=date,descr=rdata['descr'])
        return dict(success=True, title="Абонент отключен", msg="saved")

    disable._args_len = 1
    
    @check_perm('accounts.rpc_abon_balance_get')
    def balance_get(self, rdata, request):
        from abon.models import Abonent
        uid = int(rdata['uid'])
        if uid>0:
            try:
                abonent=Abonent.objects.get(pk=uid)
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой загрузки баланса', msg='abonent not found', errors='' )
            else:
                return dict(success=True, data={'balance':abonent.bill.balance_get_wo_credit(),'credit':abonent.bill.get_credit()} )
        else:
            return dict(success=True, data={'balance':None,'credit':None} )

    balance_get._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_get')
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
        
    @check_perm('accounts.rpc_abon_abon_history_get')
    @store_read
    def abon_history_get(self,rdata,request):
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
                #return abonent.catv_card.service_log.all().order_by('-date','-id')
                raw = abonent.catv_card.service_log.raw("""
                    SELECT 
                      ch1.*, ch2.cnt 
                    FROM 
                      tv_cardhistory ch1, 
                      (SELECT 
                        card_id, 
                        date, 
                        COUNT(*) AS cnt 
                      FROM 
                        tv_cardhistory 
                      WHERE 
                        card_id=%s 
                      GROUP BY 
                        date 
                      ) ch2 
                    WHERE 
                      ch1.card_id=%s AND 
                      ch1.date=ch2.date
                    ORDER BY
                      date DESC,
                      id DESC
                    """ % (abonent.catv_card.pk, abonent.catv_card.pk))
                res = []
                for line in raw:
                    obj = {}
                    obj['id'] = line.pk
                    obj['timestamp'] = line.timestamp
                    obj['date'] = line.date
                    obj['text'] = line.__unicode__()
                    obj['descr'] = line.descr
                    obj['cnt'] = line.cnt
                    res.append(obj)
                return res
            
        else:
            return dict(success=True, data={} )

    abon_history_get._args_len = 1


    @check_perm('accounts.rpc_abon_cards_set')
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
    
    @check_perm('accounts.rpc_abon_free_cards_get')
    @store_read
    def free_cards_get(self,rdata,request):
        from tv.models import Card
        card=Card.objects.filter(num__gte=0,owner__exact=None)
        return card

    free_cards_get._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_tp_get')
    @store_read
    def cards_tp_list_get(self,rdata,request):
        from tv.models import TariffPlan
        tp=TariffPlan.objects.filter(enabled__exact=True,deleted__exact=False)
        return tp

    cards_tp_list_get._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_tp_get')
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

    @check_perm('accounts.rpc_abon_cards_tp_set')
    def cards_tp_add(self,rdata,request):
        for line in rdata:
            print "%s: %s" % (line,rdata[line])
        from tv.models import Card, TariffPlan, CardService
        from datetime import datetime
        card_id=rdata['card_id']
        try:
            tp_id=int(rdata['data']['tariff'])
        except:
            return dict(success=False, title='Сбой добавления тарифов', msg='параметр неверно задан', errors='', data={}) 
        try:
            activated = datetime.strptime(rdata['data']['activated'],'%Y-%m-%dT%H:%M:%S').date()
        except:
            try:
                activated = datetime.strptime(rdata['data']['activated'],'%Y-%m-%d %H:%M:%S').date()
            except:
                activated = datetime.now()
        try:
            extra=rdata['data']['extra']
        except:
            extra = ''
        c = Card.objects.get(pk=card_id)
        cs = CardService(card=c)
        tp = TariffPlan.objects.get(pk=tp_id)
        cs.tp = tp
        cs.activated = activated
        cs.extra = extra
        cs.save()        
        return dict(success=True, data=cs.store_record() )
        #

    cards_tp_add._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_tp_set')
    def cards_tp_update(self,rdata,request):
        from tv.models import Card, TariffPlan, CardService
        from datetime import datetime        
        card_id=rdata['card_id']
        try:
            tp_id=int(rdata['data']['tariff'])
        except:
            tp_id =0
        try:
            extra=rdata['data']['extra']
        except:
            extra = ''    
        print "~"
        print extra
        cs_id=rdata['data']['id']
        try:
            activated = datetime.strptime(rdata['data']['activated'],'%Y-%m-%dT%H:%M:%S').date()
        except:
            try:
                activated = datetime.strptime(rdata['data']['activated'],'%Y-%m-%d %H:%M:%S').date()
            except:
                activated = None                
        c = Card.objects.get(pk=card_id)
        cs = CardService.objects.get(pk=cs_id)
        if tp_id>0:
            tp = TariffPlan.objects.get(pk=tp_id)
            cs.tp = tp
        if activated:
            cs.activated = activated
        cs.extra = extra
        cs.save()        
        return dict(success=True, data=cs.store_record() )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    cards_tp_update._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_tp_set')
    def cards_tp_delete(self,rdata,request):
        from tv.models import CardService        
        cs_id=rdata['cs_id']
        cs = CardService.objects.get(pk=cs_id)
        cs.delete()
        return dict(success=True, title='Удалено', msg='deleted...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    cards_tp_delete._args_len = 1

    @check_perm('accounts.rpc_abon_cards_tp_set')
    def cards_tp_activate(self,rdata,request):
        from tv.models import CardService        
        cs_id=rdata['cs_id']
        cs = CardService.objects.get(pk=cs_id)
        if not cs.card.active:
            return dict(success=False, title='Сбой Активации тарифа', msg='карточка не активирована', errors='', data={})
        cs.activate(activated=datetime.date(cs.activated))
        return dict(success=True, title='Активировано', msg='activated...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    cards_tp_activate._args_len = 1

    @check_perm('accounts.rpc_abon_cards_tp_set')
    def cards_tp_deactivate(self,rdata,request):
        from tv.models import CardService        
        cs_id=rdata['cs_id']
        cs = CardService.objects.get(pk=cs_id)
        cs.deactivate(deactivated=datetime.date(cs.activated))
        return dict(success=True, title='Деактивировано', msg='deactivated...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})
    
    cards_tp_deactivate._args_len = 1
    
    @check_perm('accounts.rpc_abon_cards_tp_set')
    def card_unbind(self,rdata,request):
        from tv.models import Card        
        card_id=rdata['card_id']
        c = Card.objects.get(pk=card_id)
        c.owner = None
        c.save()
        return dict(success=True, title='Удалено', msg='deleted...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    card_unbind._args_len = 1

    @check_perm('accounts.rpc_abon_cards_tp_set')
    def card_activate(self,rdata,request):
        from tv.models import Card        
        card_id=rdata['card_id']
        c = Card.objects.get(pk=card_id)
        c.activate(activated=datetime.date(c.activated))
        return dict(success=True, title='Активировано', msg='activated...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})

    card_activate._args_len = 1

    @check_perm('accounts.rpc_abon_cards_tp_set')
    def card_deactivate(self,rdata,request):
        from tv.models import Card        
        card_id=rdata['card_id']
        c = Card.objects.get(pk=card_id)
        c.deactivate(deactivated=datetime.date(c.activated))
        return dict(success=True, title='Деактивировано', msg='deactivated...', data={} )
        #return dict(success=False, title='Сбой загрузки тарифов', msg='not implemented yet', errors='', data={})
    
    card_deactivate._args_len = 1

    
    @check_perm('accounts.rpc_abon_payments_get')
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
            payments=Payment.objects.filter(bill=abonent.bill,rolled_by__exact=None)
            return payments.order_by('-timestamp','-pk')
        return {}
    payments_get._args_len = 1

    @check_perm('accounts.rpc_abon_fees_get')
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
            fees=Fee.objects.filter(bill=abonent.bill,rolled_by__exact=None)
            return fees.order_by('-timestamp','-pk')
        return {}
    fees_get._args_len = 1
        
    @check_perm('accounts.rpc_abon_registers_get')
    @store_read
    def registers_get(self,rdata,request):
        from tv.models import PaymentRegister
        return PaymentRegister.objects.filter(closed__exact=False).order_by('pk')
    
    registers_get._args_len = 1
        
    @check_perm('accounts.rpc_abon_registers_get_last')
    @store_read
    def registers_get_last(self,rdata,request):
        from tv.models import PaymentRegister
        from lib.functions import QuerySetChain
        opened = PaymentRegister.objects.filter(closed__exact=False)
        closed = PaymentRegister.objects.filter(closed__exact=True)[:10]
        return QuerySetChain(opened,closed)
         
    registers_get_last._args_len = 1
    
    @check_perm('accounts.rpc_abon_make_payment')
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
        #if pt.count()>0:
        #    return dict(success=False, title='Сбой проведения оплаты', msg='Возможно повторный ввод квитанции', errors='', data={} )
        
        p = Payment()
        p.register = register
        p.source = register.source
        p.bill = abonent.bill
        p.sum = sum
        p.descr = descr
        p.inner_descr = descr
        p.admin= request.user
        p.bank_date = bank_date
        p.save()
                    
        return dict(success=True, title='Оплата принята', msg='...', errors='', data={} )
    
    make_payment._args_len = 1
    
    @check_perm('accounts.rpc_abon_feetypes_get')
    @store_read
    def feetypes_get(self,rdata,request):
        from tv.models import FeeType, FEE_TYPE_ONCE
        return FeeType.objects.filter(ftype=FEE_TYPE_ONCE)
    
    feetypes_get._args_len = 1
    
    @check_perm('accounts.rpc_abon_make_fee')
    def make_fee(self,rdata,request):
        from tv.models import FeeType, Fee, Payment
        from abon.models import Abonent
        from datetime import datetime
        
        print rdata
        
        ftype_id = int(rdata['type'])
        uid = int(rdata['abonent'])
        sum = float(rdata['sum'])
        tmpdate = rdata['bankdate']
        descr = rdata['descr'] or ''        
        autopay = rdata['autopay'] or False
        autoactivate = rdata['autoactivate'] or False    
        
        try:
            ftype = FeeType.objects.get(pk=ftype_id)
        except FeeType.DoesNotExist:
            return dict(success=False, title='Сбой снятия денег', msg='register not found', errors='', data={} )

        inner_descr = "%s [%s] (%s)" % (ftype.__unicode__(),rdata['sum'],rdata['descr'] or '')
        
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
        f.descr = descr
        f.inner_descr = inner_descr
        f.admin= request.user
        f.timestamp = bank_date
        f.save()
        f.make()
        
        if autopay:
            p = Payment()
            p.register = None
            p.source = None
            p.bill = abonent.bill
            p.sum = sum
            p.descr = descr
            p.inner_descr = inner_descr
            p.admin= request.user
            p.bank_date = bank_date
            p.save()
            p.make()
        
        if autoactivate:
            if abonent.disabled:
                rdata['date'] = rdata['bankdate']
                rdata['descr'] = inner_descr
                return [
                    self.enable(rdata, request=request),
                    dict(success=True, title='Снятие проведено', msg='...', errors='', data={} )
                ]
                                
        return dict(success=True, title='Снятие проведено', msg='...', errors='', data={} )        
    
    make_fee._args_len = 1
        
    @check_perm('accounts.rpc_abon_make_transfer')
    def make_transfer(self,rdata,request):
        from tv.models import Fee, Payment
        from abon.models import Abonent
        from datetime import datetime
        
        descr = rdata['descr'] or ''
        
        if 'abonent_from' in rdata and rdata['abonent_from']>0:
            pass
        else:
            return dict(success=False, title='Сбой переносa средств', msg='Invalid option value: abonent_from', errors='', data={} ) 
        
        if 'abonent_to' in rdata and rdata['abonent_to']>0:
            pass        
        else:
            return dict(success=False, title='Сбой переносa средств', msg='Invalid option value: abonent_to', errors='', data={} )
        
        if 'sum' in rdata and rdata['sum']>0:
            pass
        else:
            return dict(success=False, title='Сбой переносa средств', msg='Invalid option value: sum', errors='', data={} )
        
        if 'date' in rdata and rdata['date']>0:
            date = rdata['date']
            try:
                date = datetime.strptime(date,'%Y-%m-%dT%H:%M:%S').date()
            except ValueError:
                return dict(success=False, title='Сбой переносa средств', msg='invalid date', errors='', data={} )
        else:
            return dict(success=False, title='Сбой переносa средств', msg='invalid date', errors='', data={} )
        try:
            abon_from = Abonent.objects.get(pk=rdata['abonent_from'])
            abon_to = Abonent.objects.get(pk=rdata['abonent_to'])
        except Abonent.DoesNotExist:
            return dict(success=False, title='Сбой переносa средств', msg='Abonent not found', errors='', data={} )
        else:
            f = Fee()            
            f.bill = abon_from.bill
            f.sum = rdata['sum']
            f.descr = 'Трансфер средств. recipient client id = %s ' % abon_to.pk
            f.inner_descr = descr
            f.admin= request.user
            f.bank_date = date
            f.save()
            f.make()
            
            p = Payment()
            p.bill = abon_to.bill
            p.sum = rdata['sum']
            p.descr = 'Трансфер средств. source client id = %s ' % abon_from.pk            
            p.inner_descr = descr
            p.admin= request.user
            p.bank_date = date
            p.save()
            p.make()
                                
        print rdata                
        return dict(success=True, title='Перенос средств успешен', msg='...', errors='', data={} )
    
    make_transfer._args_len = 1
    
    @check_perm('accounts.rpc_abon_payment_rollback')
    def payment_rollback(self,rdata,request):
        from tv.models import Payment
        if 'payment_id' in rdata and rdata['payment_id']>0:
            payment_id = rdata['payment_id']
            try:
                payment = Payment.objects.get(pk=payment_id)
            except Payment.DoesNotExist:
                return dict(success=False, title='Сбой отката оплат', msg='payment not found', errors='', data={} )
            else:                
                if payment.maked:
                    res = payment.rollback()
                    if res[0]:
                        return dict(success=True, title='Оплата удалена', msg='rolled back', errors='', data={} )
                    else:
                        return dict(success=False, title='Сбой отката оплаты', msg=res[1], errors='', data={} )
                else:                    
                    return dict(success=False, title='Сбой отката оплаты', msg='платёж еще не засчитан', errors='', data={} )
        else:
            return dict(success=False, title='Сбой отката оплат', msg='payment not found', errors='', data={} )
        
    payment_rollback._args_len = 1
    
    @check_perm('accounts.rpc_abon_fee_rollback')
    def fee_rollback(self,rdata,request):
        from tv.models import Fee
        if 'fee_id' in rdata and rdata['fee_id']>0:
            fee_id = rdata['fee_id']
            try:
                fee = Fee.objects.get(pk=fee_id)
            except Fee.DoesNotExist:
                return dict(success=False, title='Сбой отката оплат', msg='fee not found', errors='', data={} )
            else:                
                if fee.maked:
                    res = fee.rollback()
                    if res[0]:
                        return dict(success=True, title='Снятие удалена', msg='rolled back', errors='', data={} )
                    else:
                        return dict(success=False, title='Сбой отката снятия', msg=res[1], errors='', data={} )
                else:                    
                    return dict(success=False, title='Сбой отката снятия', msg='снятие еще не засчитано', errors='', data={} )
        else:
            return dict(success=False, title='Сбой отката снятия', msg='fee not found', errors='', data={} )
        
    fee_rollback._args_len = 1
    
    @check_perm('accounts.rpc_abon_reg_payments_get')
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
        
    @check_perm('accounts.rpc_abon_reg_payments_delete')
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
    
    @check_perm('accounts.rpc_abon_reg_payments_partially_confirm')
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

    @check_perm('accounts.rpc_abon_history_delete')
    def history_delete(self,rdata,request):
        from tv.models import CardHistory
        if 'history_id' in rdata and rdata['history_id']>0:
            history_id = rdata['history_id']
        try:
            ch=CardHistory.objects.get(pk=history_id)
        except CardHistory.DoesNotExist:            
            return dict(success=False, title='Сбой удаления истории', msg='card history not found', errors='', data={} )
        else:
            ch_this_day = CardHistory.objects.filter(card=ch.card,date=ch.date)
            if( ( ch_this_day.count() % 2 ) == 0 ):
                ch_this_day.delete()
                return dict(success=True, title='Удаление истории', msg='deleted', errors='', data={} )
            else:
                return dict(success=False, title='Сбой удаления истории', msg='card history delete requirements not met', errors='', data={} )
        
    history_delete._args_len = 1
                        
    @check_perm('accounts.rpc_abon_admins_get')
    @store_read
    def admins_get(self,rdata,request):
        from accounts.models import User
    
        return User.objects.all()
    
    admins_get._args_len = 1
    
    @check_perm('accounts.rpc_abon_comment_get')
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
    
    @check_perm('accounts.rpc_abon_comment_set')
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
    
    @check_perm('accounts.rpc_abon_launch_hamster')
    def launch_hamster(self, rdata, request):
        from abon.models import Abonent
        return dict(success=False, title='Сбой пересчёта баланса', msg='функция отключена', errors='')
        if 'uid' in rdata and rdata['uid']>0:
            try:
                a=Abonent.objects.get(pk=rdata['uid'])
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой пересчёта баланса', msg='abonent not found', errors='')
            else:
                a.launch_hamster(debug=False)
                return  dict(success=True, title='Пересчитано', msg='recalculated', errors='' )
        else:
            return dict(success=False, errors='')
            #return dict(success=False, title='Сбой загрузки формы', msg='abonent not found', errors='')
        
    launch_hamster._args_len = 1
    
    @check_perm('accounts.rpc_abon_abonent_delete')
    def abonent_delete(self, rdata, request):
        from abon.models import Abonent
        if 'uid' in rdata and rdata['uid']>0:
            try:
                a=Abonent.objects.get(pk=rdata['uid'])
            except Abonent.DoesNotExist:
                return dict(success=False, title='Сбой удаления', msg='abonent not found', errors='')
            else:
                if not request.user.has_perm('abon.can_delete_abonents'):
                    return dict(success=False, title='Сбой удаления', msg='действие запрещено', errors='')
                a.delete()
                return  dict(success=True, title='Удалено', msg='deleted', errors='' )
        else:
            return dict(success=False, errors='')
    
    abonent_delete._args_len = 1