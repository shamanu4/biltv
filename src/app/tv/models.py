# -*- coding: utf-8 -*-

from django.db import models
from logger.models import logging_postsave, logging_postdelete
from datetime import datetime, date

class Trunk(models.Model):

    num = models.IntegerField(default=1,unique=True)
    enabled = models.BooleanField(default = False)
    cached = models.IntegerField(default=0)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.num

    class Meta:
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
            if not slot or slot.encoded:
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

    name = models.CharField(max_length=32,default='channel name')
    bound = models.ManyToManyField(Trunk, blank=True, null=True, related_name="channels", through='TrunkChannelRelationship')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % (self.name)

    class Meta:
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
    trunk = models.ForeignKey(Trunk,related_name='slotlist')
    slot = models.IntegerField(choices=SLOT_CHOICES, blank=True, null=True)
    channel = models.ForeignKey(Channel)
    encoded = models.BooleanField(default = False)

    def save(self, *args, **kwargs):
        super(self.__class__, self).save(*args, **kwargs)
        if self.trunk:
            self.trunk.rehash()

    def __unicode__(self):
        return "%s [%s:%s]" % (self.channel.name,self.trunk.num,self.slot)

    class Meta:
        ordering = ('trunk__num','slot')
        unique_together = (('trunk', 'channel'),)


FEE_TYPE_DAILY=0
FEE_TYPE_WEEKLY=1
FEE_TYPE_MONTHLY=2
FEE_TYPE_YEARLY=3
FEE_TYPE_ONCE=4
FEE_TYPE_CUSTOM=5


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
    sum = models.FloatField(default=0)
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return u'Снятие денег | %s (%s)' % (self.name, self.sum or self.comment or u'---')

    def get_sum(self,date=None):
        from lib.functions import date_formatter
        if not self.ftype == FEE_TYPE_CUSTOM:
            return {'fee':self.sum,'ret':0}

        if not date:
            date=date_formatter()['day']
        
        print "custim fee"
        day = date.day    
        print date    
        print day        
        sum = 0
        ret = 0

        ranges = self.ranges.filter(startday__lte=day).filter(endday__gte=day)
        print ranges
        for range in ranges:
            sum += range.sum
            ret += range.ret
            
        print "sum: %s ret: %s" % (sum,ret)
        return {'fee':sum,'ret':ret}

    def store_record(self):
        obj = {}
        obj['id'] = self.pk
        obj['unicode'] = self.__unicode__()
        obj['sum'] = self.get_sum()['fee']
        return obj




class FeeCustomRanges(models.Model):

    fee_type = models.ForeignKey(FeeType, related_name='ranges')
    startday = models.PositiveSmallIntegerField()
    endday = models.PositiveSmallIntegerField()
    sum = models.FloatField(default=0)
    ret = models.FloatField(default=0)

    def __unicode__(self):
        return u'%s-%s: %s; %s;' % (self.startday, self.endday, self.sum, self.ret)



class TariffPlan(models.Model):

    name = models.CharField(max_length=64,default='tariff plan')
    channels = models.ManyToManyField(TrunkChannelRelationship,blank=True,related_name='tps',through='TariffPlanChannelRelationship')
    enabled = models.BooleanField(default=False)
    fee_list = models.ManyToManyField(FeeType,blank=True,through='TariffPlanFeeRelationship')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)

    def __unicode__(self):
        return "%s" % self.name

    def send(self):
        for service in self.services.filter(card__num__gte=0):
            service.card.send()

    def save(self, *args, **kwargs):
        print "saving tp..."
        super(self.__class__, self).save(*args, **kwargs)
        self.send()

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



class TariffPlanChannelRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan)
    chrel = models.ForeignKey(TrunkChannelRelationship, verbose_name=u'канал')

    def __unicode__(self):
        return "%s - %s [%s:%s]" % (self.tp.name, self.chrel.channel.name, self.chrel.trunk.num, self.chrel.slot)

    class Meta:
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
        return PaymentRegisterStamp.filter(register=self)

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
        return obj
        
        
    
class PaymentRegisterStamp(models.Model):
    
    register = models.ForeignKey("tv.PaymentRegister")
    admin = models.ForeignKey("accounts.User")
    confirmed = models.BooleanField(default=False)
    
    def __unicode__(self):
        return self.register.__unicode__()



class Payment(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill")
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
        obj['onwer_code'] = self.owner.get_code() or None
        obj['onwer_name'] = self.owner.person.__unicode__() or None
        obj['admin'] = self.admin.first_name or self.admin.username 
        return obj

    def make(self):
        if self.maked:
            return (True,self)
        self.prev = self.bill.balance
        self.bill.balance = self.bill.balance + self.sum
        self.bill.save()
        self.maked=True
        self.save()
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
            r.inner_descr = "rollback payment id:%s" % self.pk
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



class Fee(models.Model):

    timestamp = models.DateTimeField(default=datetime.now)
    bill = models.ForeignKey("abon.Bill")
    card = models.ForeignKey("tv.Card",blank=True,null=True)
    sum = models.FloatField(default=0)
    prev = models.FloatField(default=0)
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
        obj['maked'] = self.maked
        obj['descr'] = self.descr
        obj['inner_descr'] = self.inner_descr
        return obj

    def make(self):
        if self.maked:
            return (True,self)
        self.prev = self.bill.balance
        if self.fee_type and not self.fee_type.allow_negative:
            if self.sum > 0 and self.bill.balance - self.sum < 0:
                self.descr = "Not enough money"
                self.save()
                return (False,"Not enougn money")
        self.bill.balance = self.bill.balance - self.sum
        self.bill.save()
        self.maked=True
        self.save()
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
            r.inner_descr = "rollback fee id:%s" % self.pk
            r.save()
            r.make()
            self.rolled_by=r
            self.save()
            return (True,r)
        return (False,"Already rolled back")



class TariffPlanFeeRelationship(models.Model):

    tp = models.ForeignKey(TariffPlan, related_name="fees")
    fee_type = models.ForeignKey(FeeType)

    def __unicode__(self):
        return "%s - %s" % (self.tp.name, self.fee_type.name)

    def check_fee(self,card,fee_date=None,**kwargs):
        from lib.functions import date_formatter         
        date = date_formatter(fee_date)
        print "checking fee ..."
        print date
        my_maked_fees = Fee.objects.filter(card__exact=card, tp__exact=self.tp, fee_type__exact=self.fee_type, maked__exact=True, deleted__exact=False)
        if not card.bill:
            return (False,"This card have not account with bill")
        if self.fee_type.ftype == FEE_TYPE_ONCE:
            return self.make_fee(card,date['day'],**kwargs)

        if self.fee_type.ftype == FEE_TYPE_CUSTOM:
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
        print "making fee ..."
        fee = Fee()
        fee.bill = card.bill
        fee.card = card
        fee.tp = self.tp
        fee.fee_type = self.fee_type
        fee.sum = self.fee_type.get_sum(date)['fee']
        fee.inner_descr = "%s | %s" % (card.name, fee.fee_type.__unicode__())
        if date:
            fee.timestamp = date
        fee.save()
        if 'hold' in kwargs and kwargs['hold']:
            print "holding fee"
            return (True,fee)
        return fee.make()

    def make_ret(self,card,date=None,**kwargs):
        print "making ret ..."
        print date
        fee = Fee()
        fee.bill = card.bill
        fee.card = card
        fee.tp = self.tp
        fee.fee_type = self.fee_type
        fee.sum = - self.fee_type.get_sum(date)['ret']
        fee.inner_descr = "Money return on service deactivation"
        if date:
            fee.timestamp = date
        fee.save()
        return fee.make()

    class Meta:
        ordering = ('tp__name','fee_type__name')
        unique_together = (('tp', 'fee_type'),)


CARD_SERVICE_ACTIVATED = 0
CARD_SERVICE_DEACTIVATED = 1
CARD_SERVICE_ADDED = 2
CARD_SERVICE_REMOVED = 3
CARD_OWNER_ADDED = 4
CARD_OWNER_REMOVED = 5
CARD_OWNER_CHANGED = 6

CARD_SERVICE_ACTIONS = (
    CARD_SERVICE_ACTIVATED,
    CARD_SERVICE_DEACTIVATED,
    CARD_SERVICE_ADDED,
    CARD_SERVICE_REMOVED,
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
        (CARD_OWNER_ADDED, u'owner added'),
        (CARD_OWNER_REMOVED, u'owner removed'),
        (CARD_OWNER_CHANGED, u'owner changed'),
    )

    timestamp = models.DateTimeField(default=datetime.now)
    date = models.DateField(default=date.today)
    card = models.ForeignKey("tv.Card",related_name='service_log')
    action = models.PositiveSmallIntegerField(choices=CARD_ACTIONS)
    oid = models.PositiveIntegerField()
    descr = models.TextField()

    class Meta:
        ordering = ('-date',)
        
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

    num = models.IntegerField(unique=True)
    active = models.BooleanField(default=False)
    tps = models.ManyToManyField(TariffPlan, through='CardService')
    deleted = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)
    owner = models.ForeignKey("abon.Abonent", blank=True, null=True, related_name='cards')

    def __unicode__(self):
        return "%s" % self.num
    
    @property
    def name(self):
        if self.num > 0:
            return "Карточка %s " % self.num
        else:
            return "CaTV"

    def send(self):
        if self.num<0:
            return False
        print "sending..."
        from scrambler import scrambler
        u = scrambler.UserQuery(self.num)
        u.run()

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
        
        if old and not action == None:
            c = CardHistory()
            c.card = self
            c.date = sdate
            c.action = action
            c.oid = oid
            c.descr = descr
            c.save()

        print "saving..."

        if 'deactivation_processed' in kwargs and kwargs['deactivation_processed']:
                del kwargs['deactivation_processed']
        else:
            if not self.owner and self.pk:
                self.detach()
                self.deactivate()
        
        super(self.__class__, self).save(*args, **kwargs)

        if self.num>0:
            self.send()

    def save_formset(self, *args, **kwargs):
        print "saving formset..."
        super(self.__class__, self).save_formset(*args, **kwargs)


    @property
    def bin_flags(self):
        from functions import byte_or
        res = []
        trunks = Trunk.objects.all()
        for t in trunks:
            res.extend([0,0])
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
            return self.bill.balance
        else:
            return None

    @property
    def balance_int(self):
        return int(self.balance*100)

    @property
    def balance_rounded(self):
        return int(self.balance*100)/100.0

    @property
    def bin_balance(self):
        from functions import int_to_4byte_wrapped
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
        print "card deactivate..."
        print deactivated
        for service in self.services.all():
            service.deactivate(deactivated,descr)
        self.active=False
        self.save(deactivation_processed=True,descr=descr,sdate=deactivated)
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
    
    # WARNING! This method was used once during MIGRATION. Future uses RESTRICTED! This will cause  history DATA CORRUPT!  
    def timestamp_and_activation_fix(self):
        from django.core.exceptions import ObjectDoesNotExist
        print self
        if self.num>0:
            print "    THIS IS NOT CaTV CARD"
            return False
        try:
            print self.owner
        except ObjectDoesNotExist:
            self.detach()
            self.delete()
            print "    DELETED"
            return False            
        self.activated = self.service_log.all().order_by('timestamp')[0].timestamp
        catv_service_q = self.services.all()
        if catv_service_q:
            catv_service = catv_service_q[0]
        else:
            print "    THIS CARD HAS NO SERVICES"
            return False
        catv_service.activated = self.service_log.filter(action=CARD_SERVICE_ACTIVATED).latest(field_name="timestamp").timestamp
        if self.service_log.latest(field_name="timestamp").action == CARD_SERVICE_DEACTIVATED:
            self.active=False
            catv_service.active=False
            print "    DEACTIVATED"
        else:
            self.active=True
            catv_service.active=True
            print "    ACTIVATED"
        self.save()
        catv_service.save()
        
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


class CardService(models.Model):

    card = models.ForeignKey(Card,related_name='services')
    tp = models.ForeignKey(TariffPlan,related_name='services')
    active = models.BooleanField(default=False)
    comment = models.TextField(blank=True, null=True)
    activated = models.DateTimeField(default=datetime.now)

    def __unicode__(self):
        return "%s - %s" % (self.card.num,self.tp.name)

    def save(self, *args, **kwargs):
        action = None
        oid = None
        old = None
        if not self.pk:
            action = CARD_SERVICE_ADDED
            oid = self.tp.pk
        else:
            old = CardService.objects.get(pk=self.pk)
            if not old.active == self.active:                
                if self.active:
                    action = CARD_SERVICE_ACTIVATED
                    oid = self.tp.pk
                else:
                    action = CARD_SERVICE_DEACTIVATED
                    oid = old.tp.pk
        
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
        

        if not action == None:
            c = CardHistory()
            c.card = self.card
            c.date = sdate
            c.action = action
            c.oid = oid
            c.descr = descr
            c.save()

        super(self.__class__, self).save(*args, **kwargs)
        if self.card.num>0:
            self.card.send()

    def delete(self, *args, **kwargs):

        action = CARD_SERVICE_REMOVED
        oid = self.tp.pk

        c = CardHistory()
        c.card = self.card
        c.action = action
        c.oid = oid
        c.save()

        super(self.__class__, self).delete(*args, **kwargs)
        self.card.send()

    def activate(self,activated = None, descr =''):
        if not self.active:
            fees = self.tp.fees.all()
            print fees
            print "activation date: %s" % activated
            ok = True
            total = 0
            allow_negative = True
            prepared = []
            for fee in fees:
                if not fee.fee_type.ftype in (FEE_TYPE_ONCE, FEE_TYPE_CUSTOM ):
                    print "skipping regular fee..."
                    continue
                f = fee.check_fee(self.card,activated,hold=True)
                if f[0]: prepared.append(f[1])
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
            if ok:
                self.active=True
                self.activated=activated or date.today()
            else:
                self.deactivate()
                return False
            self.save(sdate=activated,descr=descr)
        self.check_past_activation(activated)
        return True

    def deactivate(self,deactivated = None, descr =''):
        print "card service deactivate..."
        print deactivated
        if self.active:
            fees = self.tp.fees.filter(fee_type__ftype__exact=FEE_TYPE_CUSTOM)
            for fee in fees:
                fee.make_ret(self.card,deactivated)
            self.active=False
            self.save(sdate=deactivated,descr=descr)
        return True

    def make_fees(self,date):
        for fee in self.tp.fees.all():
            print "checking"
            print fee.fee_type
            if fee.fee_type.ftype in (FEE_TYPE_DAILY, FEE_TYPE_WEEKLY, FEE_TYPE_MONTHLY, FEE_TYPE_YEARLY):
                print self.card.owner
                fee.check_fee(self.card,date)
    
    def check_past_activation(self,activated):
        from lib.functions import date_formatter, add_months
        last_fee_date = FeesCalendar.get_last_fee_date().timestamp
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
    
    
            


