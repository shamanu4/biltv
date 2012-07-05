# -*- coding: utf-8 -*-

from django.db import models
from logger.models import logging_postsave, logging_postdelete
from datetime import datetime, date, time
from app.abills.models import Tp

class Trunk(models.Model):

    num = models.IntegerField(default=1,unique=True,verbose_name=u'номер')
    enabled = models.BooleanField(default = False,verbose_name=u'включен')
    cached = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True,verbose_name=u'комментарий')

    def __unicode__(self):
        return "%s" % self.num

    class Meta:
        verbose_name=u'ствол'
        verbose_name_plural=u'стволы'
        ordering = ('num',)
        permissions = (
            ("manage_trunk", "Can manage trunks"),
        )

    @property
    def channel_mask(self):
        from lib.functions import short_to_2byte_wrapped
        return short_to_2byte_wrapped(self.cached)
    
    @property
    def slots(self):
        res = []
        for i in range(1,17):
            try:
                ch = TrunkChannelRelationship.objects.get(trunk=self,slot=i)
            except TrunkChannelRelationship.DoesNotExist:
                ch = None
            res.append(ch)
        return res

    def rehash(self):
        hash = 0
        for i,slot in enumerate(self.slots):
            #if not slot or slot.encoded:            
            if slot and slot.encoded:
                hash += (1<<i)
        self.cached=hash
        self.save(rehashed=True)

    def save(self, *args, **kwargs):
        from scrambler import scrambler
        if not 'rehashed' in kwargs or not kwargs['rehashed']:            
            self.rehash()
        else:
            del kwargs['rehashed']
            super(Trunk, self).save(*args,**kwargs)
            q = scrambler.ChannelQuery()
            q.run()



class Channel(models.Model):

    name = models.CharField(max_length=32,default='channel name',verbose_name=u'название')
    bound = models.ManyToManyField(Trunk, blank=True, null=True, related_name="channels", through='TrunkChannelRelationship')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True,verbose_name=u'комментарий')

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
        verbose_name=u'канал'
        verbose_name_plural=u'каналы'
        ordering = ('name',)
        permissions = (
            ("manage_channel", "Can manage channels"),
        )

models.signals.post_save.connect(logging_postsave, sender=Channel)
models.signals.post_delete.connect(logging_postdelete, sender=Channel)



class TrunkChannelRelationship(models.Model):
    SLOT_CHOICES = (
        (1, u'слот 1'),
        (2, u'слот 2'),
        (3, u'слот 3'),
        (4, u'слот 4'),
        (5, u'слот 5'),
        (6, u'слот 6'),
        (7, u'слот 7'),
        (8, u'слот 8'),
        (9, u'слот 9'),
        (10, u'слот 10'),
        (11, u'слот 11'),
        (12, u'слот 12'),
        (13, u'слот 13'),
        (14, u'слот 14'),
        (15, u'слот 15'),
        (16, u'слот 16'),
    )
    trunk = models.ForeignKey(Trunk,related_name='slotlist',verbose_name=u'ствол')
    slot = models.IntegerField(choices=SLOT_CHOICES, blank=True, null=True,verbose_name=u'слот')
    channel = models.ForeignKey(Channel,verbose_name=u'канал')
    encoded = models.BooleanField(default = False,verbose_name=u'закодирован')

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        if self.trunk:
            self.trunk.rehash()

    def __unicode__(self):
        return "%s [%s:%s]" % (self.channel.name,self.trunk.num,self.slot)

    class Meta:
        verbose_name=u'связь канал-ствол'
        verbose_name_plural=u'связи канал-ствол'
        ordering = ('trunk__num','slot')
        unique_together = (('trunk', 'channel'),)


FEE_TYPE_DAILY=0
FEE_TYPE_WEEKLY=1
FEE_TYPE_MONTHLY=2
FEE_TYPE_YEARLY=3
FEE_TYPE_ONCE=4
FEE_TYPE_CUSTOM=5


class FeeIntervals(models.Model):
    start = models.DateField()
    end = models.DateField(default=date(2100,1,1))
    
    @classmethod
    def last(cls):
        return cls.objects.latest('start')
    
    def __unicode__(self):
        return u'%s - %s' % (self.start, self.end)

    
class FeeType(models.Model):

    FEE_TYPES = (
        (FEE_TYPE_DAILY, u'daily'),
        (FEE_TYPE_WEEKLY, u'weekly'),
        (FEE_TYPE_MONTHLY, u'monthly'),
        (FEE_TYPE_YEARLY, u'yearly'),
        (FEE_TYPE_ONCE, u'once'),
        (FEE_TYPE_CUSTOM, u'custom'),
    )

    name = models.CharField(max_length=32,default='fee type')
    ftype = models.PositiveSmallIntegerField(choices=FEE_TYPES, default=FEE_TYPE_MONTHLY)
    allow_negative = models.BooleanField(default=True)
    proportional = models.BooleanField(default=False)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    sum = models.FloatField()
    bonus = models.FloatField(default=0)

    class Meta:
        verbose_name=u'абонплата'
        verbose_name_plural=u'абонплаты'
        
    def __unicode__(self):
        if self.sum or self.comment:
            return u'%s (%s) %s' % (self.name, self.sum or self.comment, self.marker())
        else:
            return u'%s %s' % (self.name, self.marker())

    def marker(self):
        if self.ftype == FEE_TYPE_CUSTOM: 
            return u'[tabl.]'
        else:
            return ''
    
    def get_proportion(self,date=None):
        from lib.functions import date_formatter
        from calendar import monthrange
        if not date:
            date=date_formatter()['day']
        month_size=monthrange(date.year,date.month)[1]
        return round((month_size-date.day+1)/float(month_size),6)
        
    def get_sum(self,date=None):
        from lib.functions import date_formatter
        
        sum = 0
        ret = 0        
        full = 0
        bonus = self.bonus*self.get_proportion(date)
        retbonus = self.bonus*(1-self.get_proportion(date))
        
        if not date:
            date=date_formatter()['day']
        day = date.day    
            
        if not self.ftype == FEE_TYPE_CUSTOM:
            ranges = self.ranges.filter(interval__start__lte=date).filter(interval__end__gte=date)
            if not ranges.count():
                sum = self.sum
            for range in ranges:
                sum += range.sum
            
            if self.proportional:
                sum=round(sum*self.get_proportion(date),2)
                if self.ftype==FEE_TYPE_ONCE:
                    ret=sum
            print {'fee':sum,'ret':ret,'full':sum,'bonus':bonus,'retbonus':retbonus}
            return {'fee':sum,'ret':ret,'full':sum,'bonus':bonus,'retbonus':retbonus}
        
        ranges = self.customranges.filter(interval__start__lte=date).filter(interval__end__gte=date).filter(startday__lte=day).filter(endday__gte=day)
        for range in ranges:
            sum += range.sum
            ret += range.ret
        ranges = self.ranges.filter(interval__start__lte=date).filter(interval__end__gte=date)
        for range in ranges:
            full += range.sum
        if not ranges.count():
            full = self.sum                  
        print {'fee':sum,'ret':ret,'full':sum,'bonus':bonus,'retbonus':retbonus}
        return {'fee':sum,'ret':ret,'full':full,'bonus':bonus,'retbonus':retbonus}

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['unicode'] = self.__unicode__()
        obj['sum'] = self.get_sum()['fee']
        return obj



class FeeRanges(models.Model):
    interval = models.ForeignKey(FeeIntervals, default=FeeIntervals.last)
    fee_type = models.ForeignKey(FeeType, related_name='ranges')
    sum = models.FloatField(default=0)

    class Meta:
        ordering = ('interval',)

    def __unicode__(self):
        return u'%s | %s Sum: %s;' % (self.interval.__unicode__(), self.fee_type.__unicode__(), self.sum)


class FeeCustomRanges(models.Model):
    interval = models.ForeignKey(FeeIntervals, default=FeeIntervals.last)
    fee_type = models.ForeignKey(FeeType, related_name='customranges')    
    startday = models.PositiveSmallIntegerField()
    endday = models.PositiveSmallIntegerField()
    sum = models.FloatField(default=0)
    ret = models.FloatField(default=0)    

    class Meta:
        ordering = ['startday']

    def __unicode__(self):
        return u'%s | %s Days: %s-%s Sum: %s; %s;' % (self.interval.__unicode__(), self.fee_type.__unicode__(), self.startday, self.endday, self.sum, self.ret)



class TariffPlan(models.Model):

    name = models.CharField(max_length=64,default='tariff plan', verbose_name=u'название')
    channels = models.ManyToManyField(TrunkChannelRelationship,blank=True,related_name='tps',through='TariffPlanChannelRelationship', verbose_name=u'каналы')
    enabled = models.BooleanField(default=False, verbose_name=u'включен')
    fee_list = models.ManyToManyField(FeeType,blank=True,through='TariffPlanFeeRelationship', verbose_name=u'абонплаты')
    deleted = models.BooleanField(default=False, verbose_name=u'удален')
    comment = models.TextField(blank=True, null=True, verbose_name=u'комментарий')
    
    class Meta:
        verbose_name=u'тарифный план'
        verbose_name_plural=u'тарифные планы'
        
    def __unicode__(self):
        return "%s (%s)" % (self.name,self.get_fee())

    def send(self):
        for service in self.services.filter(card__num__gte=0):
            service.card.send_one()

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        #self.send()

    def get_fee(self):
        from lib.functions import date_formatter
        s = 0
        fees = self.fee_list.filter(ftype=FEE_TYPE_MONTHLY)
        for fee in fees:
            s += fee.get_sum(date_formatter()['month'])['fee']
        return s


    @property
    def bin_flags(self):
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend([0,0])
        for ch in self.channels.all():
            shift = (ch.trunk.num-1)*2
            if ch.slot>8:
                shift+=1
                byte = ch.slot-9
            else:
                byte = ch.slot-1
            res[shift]=res[shift]|1<<byte
        return res
    
    def copy_channels(self,tp):
        for ch in tp.channels.all():
            try:
                self.channels.through(chrel=ch,tp=self).save()
            except:
                print "%s failed!" % ch
    
    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['name'] = "%s (%s)" % (self.__unicode__(),self.get_fee())
        return obj




class TariffPlanChannelRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan, verbose_name=u'тарифный план')
    chrel = models.ForeignKey(TrunkChannelRelationship, verbose_name=u'канал')

    def __unicode__(self):
        return "%s - %s [%s:%s]" % (self.tp.name, self.chrel.channel.name, self.chrel.trunk.num, self.chrel.slot)

    class Meta:
        verbose_name=u'связь канал-тариф'
        verbose_name_plural=u'связи канал-тариф'        
        ordering = ('tp__name','chrel__channel__name')
        unique_together = (('tp', 'chrel'),)        
                

class PaymentSource(models.Model):
    
    name = models.CharField(max_length="40")
    descr = models.TextField(blank=True, null=True)
    
    def __unicode__(self):
        return self.name
    
    def store_record(self):
        obj = {}
        obj['id'] = self.id
        obj['name'] = self.name
        return obj
        



class PaymentRegister(models.Model):
    
    source = models.ForeignKey("tv.PaymentSource")
    total = models.FloatField(default=0)
    closed = models.BooleanField(default=False)
    start = models.DateField(default=date.today)
    end = models.DateField(default=date.today)
    bank = models.DateField(blank=True,null=True)
            
    def __unicode__(self):
        mark = ''
        if self.closed:
            mark = ' [x]'
        return "%s. %s (%s %s) [%s]%s" % (self.pk, self.source.name, self.start, self.end, self.total, mark)

    @property
    def current(self):
        return Payment.objects.filter(register=self).aggregate(current=models.Sum('sum'))['current'] or 0
    
    def try_this_payment(self,sum):
        if not (self.current + sum) > self.total:
            return True
        return False
    
    def get_stamps(self):
        return PaymentRegisterStamp.objects.filter(register=self)

    @property
    def is_confirmed(self):
        if self.get_stamps().filter(confirmed=False).count()>0:
            return False
        return True
    
    @property
    def is_filled(self):
        return self.current == self.total 
    
    def try_close(self):
        if self.is_confirmed and self.is_filled:
            self.closed = True
            self.save()
        return self.closed
    
    @property
    def payments_total(self):
        return self.payments.all().count()
    
    @property
    def payments_maked(self):
        return self.payments.filter(maked__exact=True).count()

    @property
    def payments_maked_sum(self):
        from django.db.models import Sum
        return self.payments.filter(maked__exact=True).aggregate(payments_maked_sum=Sum('sum'))['payments_maked_sum']
    
    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['source'] = self.source.name
        obj['total'] = self.total
        #obj['current'] = self.current
        obj['closed'] = self.closed
        obj['start'] = self.start
        obj['end'] = self.end
        obj['bank'] = self.bank
        obj['unicode'] = self.__unicode__()
        obj['payments_total'] = self.payments_total
        obj['payments_maked'] = self.payments_maked
        obj['payments_maked_sum'] = self.payments_maked_sum
        return obj
        
        
    
class PaymentRegisterStamp(models.Model):
    
    register = models.ForeignKey("tv.PaymentRegister")
    admin = models.ForeignKey("accounts.User")
    confirmed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.register.__unicode__()



class Payment(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill",related_name="payments")
    sum = models.FloatField(default=0)
    prev = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    maked = models.BooleanField(default=False)
    rolled_by = models.OneToOneField("tv.Payment", blank=True, null=True)
    descr = models.TextField()
    inner_descr = models.TextField()
    admin = models.ForeignKey("accounts.User", blank=True, null=True)
    source = models.ForeignKey("tv.PaymentSource", blank=True, null=True)
    register = models.ForeignKey("tv.PaymentRegister", blank=True, null=True, related_name="payments")
    bank_date = models.DateField(default=date.today)

    def __unicode__(self):
        return "%s" % self.sum

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        for fee in self.bill.fees.filter(maked__exact=False,deleted__exact=False,rolled_by__exact=None):
            print fee
            if not fee.card or not fee.tp:
                fee.make()
            else:
                try:
                    cs = CardService.objects.get(card=fee.card,tp=fee.tp)
                except CardService.DoesNotExist:
                    pass
                else:
                    cs.activate(activated=fee.timestamp.date())
                    fee.delete()
                    #cs.activate()

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['timestamp'] = self.timestamp
        obj['bill'] = self.bill.pk
        obj['sum'] = self.sum
        obj['prev'] = self.prev
        obj['maked'] = self.maked
        obj['descr'] = self.descr
        obj['inner_descr'] = self.inner_descr
        if self.source:
            obj['source__name'] = self.source.__unicode__()
        else:
            obj['source__name'] = u'Корректировка'
        obj['bank_date'] = self.bank_date
        if self.owner:
            obj['onwer_code'] = self.owner.get_code() or None
        else:
            obj['onwer_code'] = '*** удален! ***'            
        if self.owner:
            obj['onwer_name'] = self.owner.person.__unicode__() or None
        else:
            obj['onwer_name'] = '*** удален! ***'
        obj['admin'] = self.admin.first_name or self.admin.username 
        return obj

    def make(self):
        if self.maked:
            return (True,self)
        self.prev = self.bill.balance_get()
        self.bill.balance = self.bill.balance + self.sum
        self.maked=True
        self.save()
        self.bill.save(last_operation_date=self.bank_date)
        try:
            self.register.try_close()
        except:
            #payment has no register
            pass                        
        return (True,self)

    @property
    def rolled(self):
        try:
            self.payment
        except Payment.DoesNotExist:
            if self.rolled_by:
                return True
            else:
                return False
        else:
            return True

    def rollback(self):
        if not self.rolled:
            r = Payment()
            r.sum = -self.sum
            r.bill = self.bill
            r.inner_descr = "Возврат payment id:%s" % self.pk
            r.rolled_by = self
            r.timestamp = self.timestamp
            r.save()
            r.make()            
            self.rolled_by=r
            self.save()
            return (True,r)
        return (False,"Already rolled back")

    @property    
    def owner(self):
        if not self.bill.abonents.all().count():
            return None
        else:
            return self.bill.abonents.all()[0]

    @property
    def sort(self):
        return datetime.combine(self.bank_date,time(second=1))


class Fee(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill",related_name="fees")
    card = models.ForeignKey("tv.Card",blank=True,null=True)
    sum = models.FloatField(default=0)    
    prev = models.FloatField(default=0)
    bonus = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    maked = models.BooleanField(default=False)
    rolled_by = models.OneToOneField("tv.Fee", blank=True, null=True)
    descr = models.TextField()
    inner_descr = models.TextField()
    tp = models.ForeignKey(TariffPlan, blank=True, null=True)
    fee_type = models.ForeignKey(FeeType, blank=True, null=True)
    admin = models.ForeignKey("accounts.User", blank=True, null=True)    

    def __unicode__(self):
        return "%s" % self.sum

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        
    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['timestamp'] = self.timestamp
        obj['bill'] = self.bill.pk
        obj['sum'] = self.sum
        obj['prev'] = self.prev
        obj['bonus'] = self.bonus
        obj['maked'] = self.maked
        obj['descr'] = self.descr
        obj['inner_descr'] = self.inner_descr
        try:
            obj['rolled_by'] = self.rolled_by.pk
        except:
            obj['rolled_by'] = 0
        return obj

    def make(self):
        if self.maked:
            return (True,self)
        self.prev = self.bill.balance_get()
        if self.fee_type and not self.fee_type.allow_negative:
            if self.sum > 0 and ((self.bill.balance_get() - self.sum) < -1):
                self.descr = "Not enough money (%s < %s)" % (self.bill.balance_get(),self.sum)
                self.save()
                return (False,"Not enougn money")
        self.bill.balance = self.bill.balance - self.sum
        self.maked=True
        self.save()
        self.bill.save(last_operation_date=self.timestamp)
        if self.bonus and self.card:
            print "fee promotion"
            self.card.promotion(self)
        return (True,self)

    @property
    def rolled(self):
        try:
            self.fee
        except Fee.DoesNotExist:
            if self.rolled_by:
                return True
            else:
                return False
        else:
            return True

    def rollback(self):
        if not self.rolled:
            r = Fee()
            r.sum = -self.sum
            r.bill = self.bill
            r.card = self.card
            r.tp = self.tp
            r.fee_type = self.fee_type
            r.inner_descr = "Возврат fee id:%s" % self.pk
            r.rolled_by=self
            r.timestamp = self.timestamp
            r.save()
            r.make()
            self.rolled_by=r
            self.save()
            return (True,r)
        return (False,"Already rolled back")

    @property
    def sort(self):
        return self.timestamp


class TariffPlanFeeRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan, related_name="fees")
    fee_type = models.ForeignKey(FeeType)

    class Meta:
        verbose_name=u'связь тариф-абонплата'
        verbose_name_plural=u'связи тариф-абонплата'
        ordering = ('tp__name','fee_type__name')
        unique_together = (('tp', 'fee_type'),)

    def __unicode__(self):
        return "%s - %s" % (self.tp.name, self.fee_type.name)

    def check_fee(self,card,fee_date=None,**kwargs):
        from lib.functions import date_formatter         
        date = date_formatter(fee_date)
        my_not_maked_fees = Fee.objects.filter(card__exact=card, tp__exact=self.tp, fee_type__exact=self.fee_type,maked__exact=False, deleted__exact=False, rolled_by__exact=None)
        my_not_maked_fees.delete()
        my_maked_fees = Fee.objects.filter(card__exact=card, tp__exact=self.tp, fee_type__exact=self.fee_type, deleted__exact=False, rolled_by__exact=None)
        
        if not card.bill:
            return (False,"This card have not account with bill")
        
        if self.fee_type.ftype == FEE_TYPE_ONCE:
            return self.make_fee(card,date['day'],**kwargs)
        
        if self.fee_type.ftype == FEE_TYPE_CUSTOM:
            c = my_maked_fees.filter(timestamp__gte=date['month'],sum__lt=0)
            if c.count()>0:
                return self.make_fee(card,date['day'],maked_fees=c,**kwargs)
            else:
                return self.make_fee(card,date['day'],**kwargs)            

        if self.fee_type.ftype == FEE_TYPE_DAILY:
            c = my_maked_fees.filter(timestamp__gte=date['day'])
            if c.count()>0:
                return (False,"Fee already maked")
            else:
                return self.make_fee(card,date['day'],**kwargs)

        if self.fee_type.ftype == FEE_TYPE_WEEKLY:
            c = my_maked_fees.filter(timestamp__gte=date['week'])
            if c.count()>0:
                return (False,"Fee already maked")
            else:
                return self.make_fee(card,date['week'],**kwargs)

        if self.fee_type.ftype == FEE_TYPE_MONTHLY:
            c = my_maked_fees.filter(timestamp__gte=date['month'])
            if c.count()>0:
                return (False,"Fee already maked")
            else:
                return self.make_fee(card,date['month'],**kwargs)

        if self.fee_type.ftype == FEE_TYPE_YEARLY:
            c = my_maked_fees.filter(timestamp__gte=date['year'])
            if c.count()>0:
                return (False,"Fee already maked")
            else:
                return self.make_fee(card,date['year'],**kwargs)


    def make_fee(self,card,date=None,**kwargs):        
        fee = Fee()
        fee.bill = card.bill
        fee.card = card
        fee.tp = self.tp
        fee.fee_type = self.fee_type
        if 'maked_fees' in kwargs:
            maked_fees = kwargs['maked_fees']
            maked_fee=0
            for mfee in maked_fees:
                maked_fee += mfee.sum # [!] negative value
            tmp_sum = self.fee_type.get_sum(date)['fee']
            full_sum = self.fee_type.get_sum(date)['full']
            if tmp_sum + maked_fee > 0:
                fee.sum = -maked_fee                
                fee.inner_descr = "%s | [*fix] %s" % (card.name, fee.fee_type.__unicode__())
            else:
                fee.sum = tmp_sum
                fee.inner_descr = "%s | %s" % (card.name, fee.fee_type.__unicode__())            
        else:
            fee.sum = self.fee_type.get_sum(date)['fee']
            fee.inner_descr = "%s | %s" % (card.name, fee.fee_type.__unicode__())
        if date:
            fee.timestamp = date
        fee.bonus = self.fee_type.get_sum(date)['bonus']
        fee.save()
        if 'hold' in kwargs and kwargs['hold']:
            return (True,fee)
        return fee.make()

    def make_ret(self,card,date=None,**kwargs):
        fee = Fee()
        fee.bill = card.bill
        fee.card = card
        fee.tp = self.tp
        fee.fee_type = self.fee_type
        fee.sum = - self.fee_type.get_sum(date)['ret']
        fee.bonus = - self.fee_type.get_sum(date)['retbonus']
        fee.inner_descr = "Возврат абонплаты за часть месяца"
        if date:
            fee.timestamp = date
        fee.save()
        return fee.make()
    


CARD_SERVICE_ACTIVATED = 0
CARD_SERVICE_DEACTIVATED = 1
CARD_SERVICE_ADDED = 2
CARD_SERVICE_REMOVED = 3
CARD_SERVICE_CHANGED = 7
CARD_OWNER_ADDED = 4
CARD_OWNER_REMOVED = 5
CARD_OWNER_CHANGED = 6

CARD_SERVICE_ACTIONS = (
    CARD_SERVICE_ACTIVATED,
    CARD_SERVICE_DEACTIVATED,
    CARD_SERVICE_ADDED,
    CARD_SERVICE_REMOVED,
    CARD_SERVICE_CHANGED,
)

CARD_USER_ACTIONS = (
    CARD_OWNER_ADDED,
    CARD_OWNER_REMOVED,
    CARD_OWNER_CHANGED,
)



class CardHistory(models.Model):

    CARD_ACTIONS = (
        (CARD_SERVICE_ACTIVATED, u'включён'),
        (CARD_SERVICE_DEACTIVATED, u'отключен'),
        (CARD_SERVICE_ADDED, u'добавлен'),
        (CARD_SERVICE_REMOVED, u'удалён'),
        (CARD_SERVICE_CHANGED, u'тариф'),
        (CARD_OWNER_ADDED, u'owner added'),
        (CARD_OWNER_REMOVED, u'owner removed'),
        (CARD_OWNER_CHANGED, u'owner changed'),
    )

    timestamp = models.DateTimeField(default=datetime.now)
    date = models.DateField(default=date.today)
    card = models.ForeignKey("tv.Card",related_name='service_log')
    owner = models.ForeignKey("abon.Abonent",related_name='services_log',blank=True,null=True)
    action = models.PositiveSmallIntegerField(choices=CARD_ACTIONS)
    oid = models.PositiveIntegerField()
    descr = models.TextField()

    class Meta:
        ordering = ('-date',)
    
    def save(self, *args, **kwargs):
        try:
            self.owner = self.card.owner
        except:
            self.owner = None
        super(self.__class__, self).save(*args, **kwargs)
    
    @property
    def obj_instance(self):
        from abon.models import Abonent
        if self.action in CARD_SERVICE_ACTIONS:
            try:
                return TariffPlan.objects.get(pk=self.oid)
            except TariffPlan.DoesNotExist:
                return None
        if self.action in CARD_USER_ACTIONS:
            try:
                return Abonent.objects.get(pk=self.oid)
            except TariffPlan.DoesNotExist:
                return None
        return None

    def __unicode__(self):
        return "%s | %s" % (self.get_action_display(), self.obj_instance)

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['timestamp'] = self.timestamp
        obj['date'] = self.date
        obj['text'] = self.__unicode__()
        obj['descr'] = self.descr
        return obj
    

class Card(models.Model):

    num = models.IntegerField(unique=True,verbose_name=u'номер')
    active = models.BooleanField(default=False)
    tps = models.ManyToManyField(TariffPlan, through='CardService')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)
    owner = models.ForeignKey("abon.Abonent", blank=True, null=True, related_name='cards')

    class Meta:
        verbose_name=u'карточка'
        verbose_name_plural=u'карточки'  

    def __unicode__(self):
        return "%s" % self.num
    
    @property
    def name(self):
        if self.num > 0:
            return u'Карточка %s'  % self.num
        else:
            return "CaTV"

    def send_one(self):
        if self.num<0:
            return False
        CardDigital.touch(self)
        from scrambler import scrambler
        u = scrambler.UserQuery(self.num)
        u.run()

    def send(self):
        cc = CardDigital.objects.all().order_by('id')
        for c in cc:
            c.send()

    def save(self, *args, **kwargs):

        action = None
        oid = None
        old = None

        if self.pk:            
            old = Card.objects.get(pk=self.pk)

        if not old:
            if self.owner:
                action = CARD_OWNER_ADDED
                oid = self.owner.pk
        else:
            if not old.owner == self.owner:                
                if old.owner:
                    if not self.owner:
                        action = CARD_OWNER_REMOVED
                        oid = old.owner.pk
                    else:
                        action = CARD_OWNER_CHANGED
                        oid = self.owner.pk
                else:
                    action = CARD_OWNER_ADDED
                    oid = self.owner.pk
        
        if 'descr' in kwargs:
            descr = kwargs['descr']
            del kwargs['descr']
        else:
            descr = ''
        
        if 'sdate' in kwargs:
            sdate = kwargs['sdate']
            del kwargs['sdate']
        else:
            sdate = date.today()
        
        if 'no_log' in kwargs:
            action = None
            del kwargs['no_log']
        
        if old and not action == None:
            c = CardHistory()
            c.card = self
            c.date = sdate
            c.action = action
            c.oid = oid
            c.descr = descr
            c.save()


        if 'deactivation_processed' in kwargs and kwargs['deactivation_processed']:
                del kwargs['deactivation_processed']
        else:
            if not self.owner and self.pk:
                self.detach()
                self.deactivate()
        
        super(self.__class__, self).save(*args, **kwargs)
                
        if self.num>0:
            CardDigital.touch(self)            
            self.send_one()

    def save_formset(self, *args, **kwargs):
        super(self.__class__, self).save_formset(*args, **kwargs)

    def delete(self, *args, **kwargs):
        from settings import DIGITAL_CARD_ALLOW_DELETE        
        if self.num>0:
            if DIGITAL_CARD_ALLOW_DELETE:
                super(self.__class__, self).delete(*args, **kwargs)
                CardDigital.rehash()
            else:
                print "deleting this object (%s) will cause data corrupt. ignoring..." % self
                return False
        else:
            super(self.__class__, self).delete(*args, **kwargs)
    
    @property
    def bin_flags(self):
        from lib.functions import byte_or
        import settings
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend([0,0])
        if not self.active:
            return res
        if self.balance < settings.NEGATIVE_SUM_LOCK:
            return res
        for service in self.services.all():
            if service.active:
                if res:
                    res = byte_or(res,service.tp.bin_flags)
                else:
                    res = service.tp.bin_flags
        return res

    @property
    def bill(self):
        if self.owner:
            return self.owner.bill
        else:
            return None

    @property
    def balance(self):
        if self.bill:
            return self.bill.balance_get()
        else:
            return None

    @property
    def balance_wo_credit(self):
        if self.bill:
            return self.bill.balance_get_wo_credit()
        else:
            return None

    @property
    def balance_int(self):
        return int((self.balance_wo_credit or 0)*100)

    @property
    def balance_rounded(self):
        return int((self.balance_wo_credit or 0)*100)/100.0

    @property
    def bin_balance(self):
        from lib.functions import int_to_4byte_wrapped
        return int_to_4byte_wrapped(self.balance_int)


    def activate(self,activated=None,descr=''):
        if not self.owner:
            return False
        for service in self.services.all():
            service.activate(activated,descr)
        self.active=True
        self.activated= activated or datetime.now()
        self.save(descr=descr,sdate=activated)
        return True

    def deactivate(self,deactivated=None,descr=''):
        for service in self.services.all():
            service.deactivate(deactivated,descr)
        self.active=False
        self.save(deactivation_processed=True,descr=descr,sdate=deactivated)
        if deactivated:
            self.check_past_deactivation(deactivated)
        return True

    def detach(self):
        self.services.all().delete()
        
    def make_fees(self,date):
        if not self.active or self.deleted:
            return False
        for service in self.services.all():
            service.make_fees(date)
    
    def check_past_deactivation(self,deactivated):
        fees = self.fee_set.filter(maked=True,rolled_by=None,sum__gt=0,timestamp__gt=deactivated)
        for fee in fees:
            if not fee.fee_type.ftype == FEE_TYPE_ONCE and not fee.fee_type.ftype == FEE_TYPE_CUSTOM:  
                fee.rollback()
    
    def get_service(self,tp):
        try:
            return self.services.get(tp=tp)
        except:
            return None
    
    def abills_get_user(self,login):
        from abills.models import User
        try:
            return User.objects.get(login__exact=login)
        except:            
            return None        
        
    def promotion(self,fee):
        print "card fee promotion"        
        service = self.get_service(fee.tp)
        if not service:
            print "no service for fee promotion"
            return False
        
        u = self.abills_get_user(service.extra)
        if not u:
            print "no user for fee promotion"
            return False
        u.promotion(fee)
    
    def promotion_on(self,cs,pl,timestamp):
        u = self.abills_get_user(cs.extra)
        if not u:
            print "no user for tp promotion on"
            return False
        u.promotion_on(self,cs,pl,timestamp)
    
    def promotion_off(self,cs,pl,timestamp):
        u = self.abills_get_user(cs.extra)
        if not u:
            print "no user for tp promotion off"
            return False
        u.promotion_off(self,cs,pl,timestamp)
    
    # WARNING! This method was used once during MIGRATION. Future uses RESTRICTED! This will cause  history DATA CORRUPT!  
    def timestamp_and_activation_fix(self):
        from django.core.exceptions import ObjectDoesNotExist
        if self.num>0:
            return False
        try:
            self.owner
        except ObjectDoesNotExist:
            self.detach()
            self.delete()
            return False            
        self.activated = self.service_log.filter(action=CARD_SERVICE_ACTIVATED).latest(field_name="date").timestamp
        catv_service_q = self.services.all()
        if catv_service_q:
            catv_service = catv_service_q[0]
        else:
            return False
        catv_service.activated = self.service_log.filter(action=CARD_SERVICE_ACTIVATED).order_by('-pk')[0].timestamp
        if self.service_log.all().order_by('-pk')[0].action == CARD_SERVICE_DEACTIVATED:
            self.active=False
            self.owner.disabled=True
            catv_service.active=False
        else:
            self.active=True
            self.owner.disabled=False
            catv_service.active=True
        self.save(no_log=True)
        self.owner.save()
        catv_service.save(no_log=True)
        
    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['num'] = self.num
        if self.owner:
            obj['owner'] = self.owner.__unicode__()
        else:
            obj['owner'] = '<free>'
        obj['active'] = self.active
        obj['activated'] = self.activated
        obj['deleted'] = self.deleted
        obj['comment'] = self.comment
        return obj


class CardDigital(models.Model):
    card = models.OneToOneField(Card,related_name='digital')
    
    class Meta:
        verbose_name=u'цифрокая карточка'
        verbose_name_plural=u'цифровые карточки'  

    def __unicode__(self):
        return "%s" % self.card.num
    
    @classmethod
    def touch(cls,card):
        if card.num<0:
            return False
        try:
            cls.objects.get(card=card)
        except cls.DoesNotExist:
            digicard = cls(card=card)
            digicard.save()
        return True
    
    @classmethod
    def rehash(cls):
        from django.db import connections
        cursor = connections['default'].cursor()
        cursor.execute('TRUNCATE TABLE %s;' % (cls._meta.db_table,))
        cc = Card.objects.filter(num__gt=0)
        for c in cc:
            cls.touch(c)
    
    def send(self):
        self.card.send_one()
        
    def delete(self, *args, **kwargs):
        from settings import DIGITAL_CARD_ALLOW_DELETE       
        if DIGITAL_CARD_ALLOW_DELETE:
            super(self.__class__, self).delete(*args, **kwargs)
            CardDigital.rehash()
        else:
            print "deleting this object (%s) will cause data corrupt. ignoring..." % self
            return False

            
class CardService(models.Model):

    card = models.ForeignKey(Card,related_name='services')
    tp = models.ForeignKey(TariffPlan,related_name='services')
    active = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)
    extra = models.CharField(max_length=40,blank=True, null=True)

    def __unicode__(self):
        return "%s - %s" % (self.card.num,self.tp.name)

    def save(self, *args, **kwargs):
        print 'saving service'
        action = None
        oid = None
        old = None
        
        if 'chtp' in kwargs:
            chtp = kwargs['chtp']
            del kwargs['chtp']
        else:
            chtp = False
        
        if 'sdate' in kwargs:
            sdate = kwargs['sdate']
            del kwargs['sdate']
        else:
            sdate = date.today()
            
        if 'descr' in kwargs:
            descr = kwargs['descr']
            del kwargs['descr']
        else:
            descr = date.today()
        
        if not self.pk:
            action = CARD_SERVICE_ADDED
            oid = self.tp.pk
        else:
            old = CardService.objects.get(pk=self.pk)
            if not old.tp.pk == self.tp.pk and not chtp:
                dt = self.activated
                act = old.active
                if act:
                    old.deactivate(deactivated = dt)
                    old.tp = self.tp
                    old.save(chtp=True)                
                action = CARD_SERVICE_CHANGED
                oid = self.tp.pk
                if not action == None:
                    c = CardHistory()
                    c.card = self.card
                    c.date = dt
                    c.action = action
                    c.oid = oid
                    c.descr = descr
                    c.save()                
                if act:       
                    old.activate(activated = dt)
                super(self.__class__, self).save(*args, **kwargs)
                if self.card.num>0:
                    self.card.send_one()
                return False            
            if not old.active == self.active:                
                if self.active:
                    action = CARD_SERVICE_ACTIVATED
                    oid = self.tp.pk
                else:
                    action = CARD_SERVICE_DEACTIVATED
                    oid = old.tp.pk
                
        if 'no_log' in kwargs:
            if kwargs['no_log']:
                action = None
            del kwargs['no_log']
        
        if not action == None:
            c = CardHistory()
            c.card = self.card
            c.date = sdate
            c.action = action
            c.oid = oid
            c.descr = descr
            c.save()

        super(self.__class__, self).save(*args, **kwargs)
        
        if self.active:
            self.promotion_on(self.activated)
        else:
            self.promotion_off(self.activated)
        if self.card.num>0:
            self.card.send_one()

    def delete(self, *args, **kwargs):

        action = CARD_SERVICE_REMOVED
        oid = self.tp.pk

        c = CardHistory()
        c.card = self.card
        c.action = action
        c.oid = oid
        c.save()

        super(self.__class__, self).delete(*args, **kwargs)
        self.card.send_one()
    
    def check_negative(self,fees,date,fee_types_allowed):
            print fees
            ok = True
            total = 0
            allow_negative = True
            prepared = []
            for fee in fees:
                print "cycle" 
                print fee
                print fee.fee_type.ftype
                if not fee.fee_type.ftype in fee_types_allowed:
                    continue                
                f = fee.check_fee(self.card,date,hold=True)
                print f
                if f[0]: prepared.append(f[1])
            print "prepared fees:"
            print prepared
            for fee in prepared:
                allow_negative = allow_negative and fee.fee_type.allow_negative
                total += fee.sum
            if allow_negative or (total>0 and self.card.balance - total >0):
                for fee in prepared:
                    ok = ok and fee.make()[0]
            else:
                ok = False
                for fee in prepared:
                    fee.inner_descr = "Not enough money"
                    fee.save()
            return (ok,prepared,total)
                    
    def activate(self,activated = None, descr ='', no_log=False):
        print 'activating service'
        print activated
        print self.active
        if not self.active:
            fees = self.tp.fees.all()
            (ok,prepared,total) = self.check_negative(fees,activated,(FEE_TYPE_ONCE, FEE_TYPE_CUSTOM))
            if ok:
                self.active=True
                self.activated=activated or date.today()
            else:
                self.deactivate()
                return False
            self.promotion_on(activated)
            self.save(sdate=activated,descr=descr,no_log=no_log)
        if isinstance(activated,datetime):
            activated = activated.date()
        self.check_past_activation(activated)
        return True

    def deactivate(self,deactivated = None, descr =''):
        from django.db.models import Q
        print 'deactivating service'
        print deactivated
        if self.active:
            fees = self.tp.fees.filter(Q(fee_type__ftype__exact=FEE_TYPE_CUSTOM)|Q(fee_type__proportional__exact=True,fee_type__ftype__exact=FEE_TYPE_ONCE))
            for fee in fees:
                fee.make_ret(self.card,deactivated)
            self.active=False
            self.promotion_off(deactivated)
            self.save(sdate=deactivated,descr=descr)
        return True
    
    def promotion_link_get(self):
        try:
            pl = PromotionLink.objects.get(tp=self.tp)
        except PromotionLink.DoesNotExist:
            return None
        else:
            return pl
    
    def promotion_link_disabled_get(self):
        try:
            pl = PromotionLink.objects.get(tp__exact=None)
        except PromotionLink.DoesNotExist:
            return None
        else:
            return pl
    
    def promotion_on(self,activated):
        pl = self.promotion_link_get()
        if pl:
            self.card.promotion_on(self,pl,activated)
                
    def promotion_off(self,deactivated):
        pl = self.promotion_link_disabled_get()
        if pl:
            self.card.promotion_off(self,pl,deactivated)

    def make_fees(self,date):
        fees = self.tp.fees.all()
        (ok,prepared,total) = self.check_negative(fees,date,(FEE_TYPE_DAILY, FEE_TYPE_WEEKLY, FEE_TYPE_MONTHLY, FEE_TYPE_YEARLY))
        if not ok:
            self.active = False
            self.save()
            
                
    def check_past_activation(self,activated):
        from lib.functions import date_formatter, add_months
        last_fee_date = FeesCalendar.get_last_fee_date().timestamp
        if not activated:
            activated = date.today()
        if activated < last_fee_date:
            next_fee_date = add_months(date_formatter(activated)['month'].date(),1)
            self.make_fees(next_fee_date)
            self.check_past_activation(next_fee_date)
        else:
            return True
        
    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['tariff'] = self.tp.__unicode__()
        obj['active'] = self.active
        obj['activated'] = self.activated
        obj['comment'] = self.comment
        obj['extra'] = self.extra
        return obj

    
class FeesCalendar(models.Model):
    
    timestamp = models.DateField(default=date.today)
    
    class Meta:
        ordering = ('-timestamp',)
    
    def __unicode__(self):
        return "%s" % self.timestamp
    
    @classmethod
    def get_last_fee_date(cls):
        return cls.objects.latest('timestamp')

    @classmethod
    def check_next_fee(cls,date):
        from lib.functions import date_formatter
        month = date_formatter(date)['month']
        if cls.get_last_fee_date().timestamp < month.date():
            return True
        else:
            return False
          
    @classmethod
    def make_fees(cls,date):
        from abon.models import Abonent
        active = Abonent.objects.filter(disabled__exact=False, deleted__exact=False)
        for abonent in active:
            abonent.make_fees(date)
    
    @classmethod
    def push_next_fee(cls,date):
        if cls.check_next_fee(date):
            from lib.functions import date_formatter
            month = date_formatter(date)['month']
            cls.make_fees(month)            
            instance = cls(timestamp=month)
            instance.save()    
    
    
    
class PromotionLink(models.Model):

    tp = models.ForeignKey(TariffPlan,related_name='promotions',unique=True,blank=True,null=True)
    abills_tp_id = models.IntegerField(choices=Tp.choices(),db_column="abills_tp_id") 

    @property
    def abills_tp(self):
        from abills.models import Tp
        try:
            return Tp.objects.get(pk=self.abills_tp_id)
        except:
            return None 



class  PaymentAutoMake(models.Model):

    register = models.OneToOneField(PaymentRegister)

    def __unicode__(self):
        return self.register.__unicode__()
